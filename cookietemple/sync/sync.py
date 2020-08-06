#!/usr/bin/env python
"""
Synchronise a project TEMPLATE branch with the template.
"""
import fnmatch
import sys
from configparser import ConfigParser, NoSectionError
from distutils.dir_util import copy_tree
import git
import json
import os
import requests
import shutil
import tempfile
from pathlib import Path
from packaging import version
from rich import print

from cookietemple.create.github_support import decrypt_pat, load_github_username
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.create.create import choose_domain
from cookietemple.common.version import load_project_template_version_and_handle, load_ct_template_version


class SyncException(Exception):
    """Exception raised when there was an error with TEMPLATE branch synchronisation
    """

    pass


class PullRequestException(Exception):
    """Exception raised when there was an error creating a Pull-Request on GitHub.com
    """

    pass


class TemplateSync:
    """
    Object to hold syncing information and results.

    Args:
        project_dir (str): The path to the cookietemple project root directory
        from_branch (str): Original branch
        make_pr (bool): Set this to `True` to create a GitHub pull-request with the changes
        gh_username (str): GitHub username

    Attributes:
        project_dir (str): Path to target project directory
        from_branch (str): Original branch
        original_branch (str): Repo branch that was checked out before we started.
        made_changes (bool): Whether making the new template project introduced any changes
        make_pr (bool): Whether to try to automatically make a PR on GitHub.com
        gh_username (str): GitHub username
    """

    def __init__(self, project_dir, from_branch=None, make_pr=True, gh_username=None, token=None, major_update=False, minor_update=False):
        self.project_dir = os.path.abspath(project_dir)
        self.from_branch = from_branch
        self.original_branch = None
        self.made_changes = False
        self.make_pr = make_pr
        self.gh_pr_returned_data = {}
        self.major_update = major_update
        self.minor_update = minor_update
        self.gh_username = gh_username if gh_username else load_github_username()
        self.token = token if token else decrypt_pat()
        self.dot_cookietemple = {}

    def sync(self):
        """
        Find workflow attributes, create a new template project on TEMPLATE
        """
        self.inspect_sync_dir()
        self.checkout_template_branch()
        self.delete_template_branch_files()
        self.make_template_project()
        self.commit_template_changes()

        # Push and make a pull request if we've been asked to
        if self.made_changes and self.make_pr:
            try:
                self.push_template_branch()
                self.make_pull_request()
            except PullRequestException as e:
                self.reset_target_dir()
                raise PullRequestException(e)

        self.reset_target_dir()

        if not self.made_changes:
            print("[bold blue]No changes made to TEMPLATE - sync complete")

    def inspect_sync_dir(self):
        """
        Takes a look at the target directory for syncing. Checks that it's a git repo
        and makes sure that there are no uncommitted changes.
        """
        if not os.path.exists(os.path.join(str(self.project_dir), '.cookietemple.yml')):
            print(f'[bold red]{self.project_dir} does not appear to contain a .cookietemple.yml file. Did you delete it?')
            sys.exit(1)
            # store .cookietemple.yml content for later reuse in the dry create run
        self.dot_cookietemple = load_yaml_file(os.path.join(str(self.project_dir), '.cookietemple.yml'))
        # Check that the project_dir is a git repo
        try:
            self.repo = git.Repo(self.project_dir)
        except git.exc.InvalidGitRepositoryError as e:
            raise SyncException(f"[bold red]{self.project_dir} does not appear to be a git repository")

        # get current branch so we can switch back later
        self.original_branch = self.repo.active_branch.name
        print(f"[bold blue]Original Project repository branch is {self.original_branch}")

        # Check to see if there are uncommitted changes on current branch
        if self.repo.is_dirty(untracked_files=True):
            raise SyncException("[bold red]Uncommitted changes found in Project directory!\nPlease commit these before running cookietemple sync")

    def checkout_template_branch(self):
        """
        Try to check out the origin/TEMPLATE in a new TEMPLATE branch.
        If this fails, try to check out an existing local TEMPLATE branch.
        """
        try:
            self.from_branch = self.repo.active_branch.name
        except git.exc.GitCommandError as e:
            print(f"[bold red]Could not find active repo branch:\n{e}")
        # Try to check out the `TEMPLATE` branch
        try:
            self.repo.git.checkout("origin/TEMPLATE", b="TEMPLATE")
        except git.exc.GitCommandError:
            # Try to check out an existing local branch called TEMPLATE
            try:
                self.repo.git.checkout("TEMPLATE")
            except git.exc.GitCommandError:
                raise SyncException("[bold red]Could not check out branch 'origin/TEMPLATE' or 'TEMPLATE'")

    def delete_template_branch_files(self):
        """
        Delete all files in the TEMPLATE branch
        """
        # Delete everything
        print("[bold blue]Deleting all files in TEMPLATE branch")
        for the_file in os.listdir(self.project_dir):
            if the_file == ".git":
                continue
            file_path = os.path.join(self.project_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise SyncException(e)

    def make_template_project(self):
        """
        Delete all files and make a fresh template.
        """
        print("Making a new template project.")
        # dry create run from dot_cookietemple in tmp directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # TODO REFACTOR THIS BY PASSING A PATH PARAM TO CHOOSE DOMAIN WHICH DEFAULTS TO CWD WHEN NOT PASSED (INITIAL CREATE)
            old_cwd = str(Path.cwd())
            os.chdir(tmpdirname)
            choose_domain(domain=None, dot_cookietemple=self.dot_cookietemple)
            os.remove(f'{tmpdirname}/{self.dot_cookietemple["project_slug"]}/.github/workflows/sync_project.yml')
            # copy into the cleaned TEMPLATE branch's project directory
            copy_tree(os.path.join(tmpdirname, self.dot_cookietemple['project_slug']), str(self.project_dir))
            os.chdir(old_cwd)

    def commit_template_changes(self):
        """
        If we have any changes with the new template files, make a git commit
        """
        # Check that we have something to commit
        if not self.repo.is_dirty(untracked_files=True):
            print("[bold blue]Template contains no changes - no new commit created")
            return False
        # Commit changes
        try:
            # git add only non-blacklisted files
            changed_files = [item.a_path for item in self.repo.index.diff(None)]
            globs = self.get_blacklisted_sync_globs()
            blacklisted_changed_files = []
            for pattern in globs:
                # keep track of all blacklisted files
                blacklisted_changed_files += fnmatch.filter(changed_files, pattern)
            print('[bold blue]Staging template.')
            # check for every file that its not a blacklisted file
            files_to_add = [file for file in changed_files if file not in blacklisted_changed_files]
            self.repo.git.add(files_to_add)
            # checkout changes to blacklisted files
            self.repo.index.checkout(blacklisted_changed_files, force=True)
            self.repo.index.commit("Template update for your cookietemple project.")
            self.made_changes = True
            print("[bold blue]Committed changes to TEMPLATE branch")
        except Exception as e:
            raise SyncException(f"[bold red]Could not commit changes to TEMPLATE:\n{e}")
        return True

    def push_template_branch(self):
        """If we made any changes, push the TEMPLATE branch to the default remote
        and try to make a PR. If we don't have the auth token, try to figure out a URL
        for the PR and print this to the console.
        """
        print(f"[bold blue]Pushing TEMPLATE branch to remote: {os.path.basename(self.project_dir)}")
        try:
            print(self.project_dir)
            origin = self.repo.remote('origin')
            self.repo.head.ref.set_tracking_branch(origin.refs.TEMPLATE)
            print(self.repo.remotes)
            self.repo.git.push()
        except git.exc.GitCommandError as e:
            raise PullRequestException(f"Could not push TEMPLATE branch:\n{e}")

    def make_pull_request(self):
        """
        Create a pull request to a base branch from a head branch (default: TEMPLATE)
        """
        if self.dot_cookietemple['is_github_orga']:
            self.gh_username = self.dot_cookietemple['github_orga']
        pr_title = "Important! Template update for your cookietemple project's template."
        pr_body_text = (
            "A new release of the main template in cookietemple has just been released. "
            "This automated pull-request attempts to apply the relevant updates to this Project.\n\n"
            "Please make sure to merge this pull-request as soon as possible. "
            "Once complete, make a new minor release of your Project.")

        # Try to update an existing pull-request
        # TODO CT CODE FOR CHECK IF PR ALREADY EXISTS
        self.submit_pull_request(pr_title, pr_body_text)

    def submit_pull_request(self, pr_title, pr_body_text):
        """
        Create a new pull-request on GitHub
        """
        pr_content = {
            "title": pr_title,
            "body": pr_body_text,
            "maintainer_can_modify": True,
            "head": "TEMPLATE",
            "base": self.from_branch,
        }

        r = requests.post(
            url=f"https://api.github.com/repos/{self.gh_username}/{self.dot_cookietemple['project_slug']}/pulls",
            data=json.dumps(pr_content),
            auth=requests.auth.HTTPBasicAuth(self.gh_username, self.token),
        )
        try:
            self.gh_pr_returned_data = json.loads(r.content)
            returned_data_prettyprint = json.dumps(self.gh_pr_returned_data, indent=4)
        except:
            self.gh_pr_returned_data = r.content
            returned_data_prettyprint = r.content

        # PR worked
        if r.status_code == 201:
            print('[bold blue]Successfully created PR!')

        # Something went wrong
        else:
            raise PullRequestException(f"GitHub API returned code {r.status_code}: \n{returned_data_prettyprint}")

    def check_sync_level(self) -> bool:
        """
        Check whether a pull request should be made according to the set level in the cookietemple.cfg file.
        Possible levels are:
            - minor: Create a pull request if it's a minor or major change
            - major: Create a pull request only if it's a major change
        :return: Whether the changes level is equal to or smaller than the set sync level; whether a PR should be created or not
        """
        try:
            parser = ConfigParser()
            parser.read(f'{self.project_dir}/cookietemple.cfg')
            level_item = list(parser.items('sync_level'))
            # check for proper configuration if the sync_level section (only one item named ct_sync_level with valid levels major or minor
            if len(level_item) != 1 or 'ct_sync_level' not in level_item[0][0] or not any(level_item[0][1] == valid_lvl for valid_lvl in ['major', 'minor']):
                print('[bold red]Your sync_level section is missconfigured. Make sure that it only contains one item named ct_sync_level with only valid levels'
                      ' like minor or major!')
                sys.exit(1)
            # check in case of minor update that level is not set to major (major case must not be handled as level is a lower bound)
            if self.minor_update:
                return level_item[0][1] != 'major'
            else:
                return True
        # cookietemple.cfg file was not found or has no section sync_level
        except NoSectionError:
            print('[bold red]Could not read from cookietemple.cfg file. Make sure your specified path contains a cookietemple.cfg file and has a sync_level '
                  'section!')
            sys.exit(1)

    def get_blacklisted_sync_globs(self) -> list:
        """
        Get all blacklisted globs from the cookietemple.cfg file.
        :return: A list of all blacklisted globs for sync (file (types) that should not be included into the sync pull request)
        """
        try:
            parser = ConfigParser()
            parser.read(f'{self.project_dir}/cookietemple.cfg')
            globs = list(parser.items('sync_files_blacklisted'))
            return [glob[1] for glob in globs]

        # cookietemple.cfg file was not found or has no section called sync_files_blacklisted
        except NoSectionError:
            print('[bold red]Could not read from cookietemple.cfg file. Make sure your specified path contains a cookietemple.cfg file and has a '
                  'sync_files_blacklisted section!')
            sys.exit(1)

    def reset_target_dir(self):
        """
        Reset the target project directory. Check out the original branch.
        """
        print(f"[bold blue]Checking out original branch: {self.original_branch}")
        try:
            self.repo.git.checkout(self.original_branch)
        except git.exc.GitCommandError as e:
            raise SyncException(f"[bold red]Could not reset to original branch {self.from_branch}:\n{e}")

    def has_major_minor_template_version_changed(self, project_dir: Path) -> (bool, bool, str, str):
        """
        Check, if the cookietemple template has been updated since last check/sync of the user.

        :return: Both false if no versions changed or a micro change happened (for ex. 1.2.3 to 1.2.4). Return is_major_update True if a major version release
        happened for the cookietemple template (for example 1.2.3 to 2.0.0). Return is_minor_update True if a minor change happened (1.2.3 to 1.3.0).
        cookietemple will use this to decide which syncing strategy to apply. Also return both versions.
        """
        template_version_last_sync, template_handle = self.sync_load_project_template_version_and_handle(project_dir)
        template_version_last_sync = version.parse(template_version_last_sync)
        current_ct_template_version = version.parse(self.sync_load_template_version(template_handle))
        # check if a major change happened (for example 1.2.3 to 2.0.0)
        is_major_update = True if template_version_last_sync.major < current_ct_template_version.major else False
        # check if minor update happened (for example 1.2.3 to 1.3.0)
        is_minor_update = True if template_version_last_sync.minor < current_ct_template_version.minor else False
        return is_major_update, is_minor_update, str(template_version_last_sync), str(current_ct_template_version)

    def sync_load_template_version(self, handle: str) -> str:
        """
        Load the version of the template available from cookietemple specified by the handler for syncing.

        :param handle: The template handle
        :return: The actual version number of the template in cookietemple
        """
        top_path = f'{os.path.dirname(__file__)}/..'
        available_templates_path = f'{str(top_path)}/create/templates/available_templates.yml'
        return load_ct_template_version(handle, available_templates_path)

    def sync_load_project_template_version_and_handle(self, project_dir: Path) -> str:
        """
        Return the project template version since last sync for user (if no sync happened, return initial create version of the template)

        :param project_dir: Top level path to users project directory
        """
        return load_project_template_version_and_handle(project_dir)
