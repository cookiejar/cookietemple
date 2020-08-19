#!/usr/bin/env python
"""
Synchronise a project TEMPLATE branch with the template.
"""
import fnmatch
import sys
from configparser import ConfigParser, NoSectionError
from distutils.dir_util import copy_tree
from subprocess import Popen, PIPE
import git
import json
import os
import requests
import shutil
import tempfile
from pathlib import Path
from packaging import version
from rich import print

from cookietemple.create.github_support import decrypt_pat, load_github_username, create_sync_secret
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.create.create import choose_domain
from cookietemple.common.version import load_project_template_version_and_handle, load_ct_template_version
from cookietemple.config.config import ConfigCommand
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple


class TemplateSync:
    """
    Hold syncing information and results.

    project_dir (str): The path to the cookietemple project root directory
    from_branch (str): Original branch
    project_dir (str): Path to target project directory
    from_branch (str): Original branch
    original_branch (str): Repo branch that was checked out before we started.
    made_changes (bool): Whether making the new template project introduced any changes
    gh_username (str): GitHub username
    patch_update (bool): Whether a patch update was found for the template or not
    minor_update (bool): Whether a minor update was found for the template or not
    major_update (bool): Whether a major update was found for the template or not
    repo_owner (str): Owner of the repo (either orga name or personal github username)
    """

    def __init__(self, project_dir, from_branch=None, gh_username=None, token=None, major_update=False, minor_update=False, patch_update=False):
        self.project_dir = os.path.abspath(project_dir)
        self.from_branch = from_branch
        self.original_branch = None
        self.made_changes = False
        self.gh_pr_returned_data = {}
        self.major_update = major_update
        self.minor_update = minor_update
        self.patch_update = patch_update
        self.gh_username = gh_username if gh_username else load_github_username()
        self.token = token if token else decrypt_pat()
        self.dot_cookietemple = {}
        self.repo_owner = self.gh_username

    def sync(self):
        """
        Sync the cookietemple project
        """
        self.inspect_sync_dir()
        self.checkout_template_branch()
        self.delete_template_branch_files()
        self.make_template_project()
        self.commit_template_changes()

        # Push and make a pull request
        if self.made_changes:
            try:
                self.push_template_branch()
                self.make_pull_request()
            except Exception as e:
                self.reset_target_dir()
                print(f'[bold red]{e}')
                sys.exit(1)

        self.reset_target_dir()

        if not self.made_changes:
            print('[bold blue]No changes made to TEMPLATE - sync complete')

    def inspect_sync_dir(self):
        """
        Examines target directory to sync, verifies that it's a git repository and ensures that there are no uncommitted changes.
        """
        if not os.path.exists(os.path.join(str(self.project_dir), '.cookietemple.yml')):
            print(f'[bold red]{self.project_dir} does not appear to contain a .cookietemple.yml file. Did you delete it?')
            sys.exit(1)
            # store .cookietemple.yml content for later reuse in the dry create run
        self.dot_cookietemple = load_yaml_file(os.path.join(str(self.project_dir), '.cookietemple.yml'))
        # Check that the project_dir is a git repo
        try:
            self.repo = git.Repo(self.project_dir)
        except git.exc.InvalidGitRepositoryError:
            print(f'[bold red]{self.project_dir} does not appear to be a git repository.')
            sys.exit(1)

        # get current branch so we can switch back later
        self.original_branch = self.repo.active_branch.name
        print(f'[bold blue]Original Project repository branch is {self.original_branch}')

        # Check to see if there are uncommitted changes on current branch
        if self.repo.is_dirty(untracked_files=True):
            print('[bold red]Uncommitted changes found in Project directory!\nPlease commit these before running cookietemple sync')
            sys.exit(1)

    def checkout_template_branch(self):
        """
        Try to check out the origin/TEMPLATE in a new TEMPLATE branch.
        If this fails, try to check out an existing local TEMPLATE branch.
        """
        try:
            self.from_branch = self.repo.active_branch.name
        except git.exc.GitCommandError as e:
            print(f'[bold red]Could not find active repo branch:\n{e}')
        # Try to check out the `TEMPLATE` branch
        try:
            self.repo.git.checkout('origin/TEMPLATE', b='TEMPLATE')
        except git.exc.GitCommandError:
            # Try to check out an existing local branch called TEMPLATE
            try:
                self.repo.git.checkout('TEMPLATE')
            except git.exc.GitCommandError:
                print('[bold red]Could not check out branch "origin/TEMPLATE" or "TEMPLATE"')
                sys.exit(1)

    def delete_template_branch_files(self):
        """
        Delete all files in the TEMPLATE branch
        """
        # Delete everything
        print('[bold blue]Deleting all files in TEMPLATE branch')
        for the_file in os.listdir(self.project_dir):
            if the_file == '.git':
                continue
            file_path = os.path.join(self.project_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'[bold red]{e}')
                sys.exit(1)

    def make_template_project(self):
        """
        Delete all files and make a fresh template.
        """
        print('[bold blue]Creating a new template project.')
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
            print('[bold blue]Template contains no changes - no new commit created')
            return False
        # Commit changes
        try:
            # git add only non-blacklisted files
            print('[bold blue]Staging template.')
            self.repo.git.add(A=True)
            changed_files = [item.a_path for item in self.repo.index.diff('HEAD')]
            globs = self.get_blacklisted_sync_globs()
            blacklisted_changed_files = []
            for pattern in globs:
                # keep track of all staged files matching a glob from the cookietemple.cfg file
                # those files will be excluded from syncing but will still be available in every new created projects
                blacklisted_changed_files += fnmatch.filter(changed_files, pattern)
            print('[bold blue]Committing changes of non blacklisted files.')
            files_to_commit = [file for file in changed_files if file not in blacklisted_changed_files]
            Popen(['git', 'commit', '-m', 'Cookietemple sync', *files_to_commit], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print('[bold blue] Stashing and saving TEMPLATE branch changes!')
            Popen(['git', 'stash'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            self.made_changes = True
            print('[bold blue]Committed changes to TEMPLATE branch')
        except Exception as e:
            print(f'[bold red]Could not commit changes to TEMPLATE:\n{e}')
            sys.exit(1)
        return True

    def push_template_branch(self):
        """
        If we made any changes, push the TEMPLATE branch to the default remote
        and try to make a PR.
        """
        print(f'[bold blue]Pushing TEMPLATE branch to remote: {os.path.basename(self.project_dir)}')
        try:
            origin = self.repo.remote('origin')
            self.repo.head.ref.set_tracking_branch(origin.refs.TEMPLATE)
            self.repo.git.push()
        except git.exc.GitCommandError as e:
            print(f'Could not push TEMPLATE branch:\n{e}')
            sys.exit(1)

    def make_pull_request(self):
        """
        Create a pull request to a base branch from a head branch (default: TEMPLATE)
        """
        if self.dot_cookietemple['is_github_orga']:
            self.repo_owner = self.dot_cookietemple['github_orga']
        pr_title = 'Important! Template update for your cookietemple project\'s template.'
        pr_body_text = (
            'A new release of the main template in cookietemple has just been released. '
            'This automated pull-request attempts to apply the relevant updates to this Project.\n\n'
            'Please make sure to merge this pull-request as soon as possible. '
            'Once complete, make a new minor release of your Project.')

        # Only create PR if it does not already exist
        if not self.check_pull_request_exists():
            self.submit_pull_request(pr_title, pr_body_text)
        else:
            print('[bold blue]An open cookietemple sync PR already exists at your repo. Changes were added to the existing PR!')

    def submit_pull_request(self, pr_title, pr_body_text):
        """
        Create a new pull-request on GitHub
        """
        pr_content = {
            'title': pr_title,
            'body': pr_body_text,
            'maintainer_can_modify': True,
            'head': 'TEMPLATE',
            'base': self.from_branch,
        }

        r = requests.post(
            url=f'https://api.github.com/repos/{self.repo_owner}/{self.dot_cookietemple["project_slug"]}/pulls',
            data=json.dumps(pr_content),
            auth=requests.auth.HTTPBasicAuth(self.gh_username, self.token),
        )
        try:
            self.gh_pr_returned_data = json.loads(r.content)
            returned_data_prettyprint = json.dumps(self.gh_pr_returned_data, indent=4)
        except requests.RequestException:
            self.gh_pr_returned_data = r.content
            returned_data_prettyprint = r.content

        # PR worked
        if r.status_code == 201:
            print('[bold blue]Successfully created PR!')

        # Something went wrong
        else:
            print(f'GitHub API returned code {r.status_code}: \n{returned_data_prettyprint}')
            sys.exit(1)

    def check_pull_request_exists(self) -> bool:
        """
        Check, if a cookietemple sync PR is already pending. If so, just push changes and do not create a new PR!

        :return Whether a cookietemple sync PR is already open or not
        """
        state = {'state': 'open'}
        query_url = f'https://api.github.com/repos/{self.repo_owner}/{self.dot_cookietemple["project_slug"]}/pulls'
        headers = {'Authorization': f'token {self.token}'}
        # query all open PRs
        r = requests.get(query_url, headers=headers, data=json.dumps(state))
        query_data = r.json()
        # iterate over the open PRs of the repo to check if a cookietemple sync PR is open
        for pull_request in query_data:
            if pull_request['title'] == 'Important! Template update for your cookietemple project\'s template.':
                return True
        return False

    def check_sync_level(self) -> bool:
        """
        Check whether a pull request should be made according to the set level in the cookietemple.cfg file.
        Possible levels are:
            - patch: Always create a pull request (lower bound)
            - minor: Create a pull request if it's a minor or major change
            - major: Create a pull request only if it's a major change
        :return: Whether the changes level is equal to or smaller than the set sync level; whether a PR should be created or not
        """
        try:
            parser = ConfigParser()
            parser.read(f'{self.project_dir}/cookietemple.cfg')
            level_item = list(parser.items('sync_level'))
            # check for proper configuration if the sync_level section (only one item named ct_sync_level with valid levels major or minor
            if len(level_item) != 1 or 'ct_sync_level' not in level_item[0][0] or not any(level_item[0][1] == valid_lvl for valid_lvl in
                                                                                          ['major', 'minor', 'patch']):
                print('[bold red]Your sync_level section is missconfigured. Make sure that it only contains one item named ct_sync_level with only valid levels'
                      ' patch, minor or major!')
                sys.exit(1)
            # check in case of minor update that level is not set to major (major case must not be handled as level is a lower bound)
            if self.patch_update:
                return level_item[0][1] != 'minor' and level_item[0][1] != 'major'
            elif self.minor_update:
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
        print(f'[bold blue]Checking out original branch: {self.original_branch}')
        try:
            self.repo.git.checkout(self.original_branch)
        except git.exc.GitCommandError as e:
            print(f'[bold red]Could not reset to original branch {self.from_branch}:\n{e}')
            sys.exit(1)

    @staticmethod
    def update_sync_token(project_name: str, gh_username=load_yaml_file(ConfigCommand.CONF_FILE_PATH)['github_username']) -> None:
        """
        Update the sync token secret for the repository.

        :param project_name Name of the users project
        :param gh_username The Github username (only gets passed, if the repo is an orga repo)
        """
        # get the personal access token for user authentification
        updated_sync_token = cookietemple_questionary_or_dot_cookietemple('password', 'Please enter your updated sync token value')
        print(f'[bold blue]\nUpdating sync secret for project {project_name}.')
        create_sync_secret(gh_username, project_name, updated_sync_token)
        print(f'[bold blue]\nSuccessfully updated sync secret for project {project_name}.')

    def has_template_version_changed(self, project_dir: Path) -> (bool, bool, bool, str, str):
        """
        Check, if the cookietemple template has been updated since last check/sync of the user.

        :return: Both false if no versions changed or a micro change happened (for ex. 1.2.3 to 1.2.4). Return is_major_update True if a major version release
        happened for the cookietemple template (for example 1.2.3 to 2.0.0). Return is_minor_update True if a minor change happened (1.2.3 to 1.3.0).
        Return is_patch_update True if its a micro update (for example 1.2.3 to 1.2.4).
        cookietemple will use this to decide which syncing strategy to apply. Also return both versions.
        """
        template_version_last_sync, template_handle = self.sync_load_project_template_version_and_handle(project_dir)
        template_version_last_sync = version.parse(template_version_last_sync)
        current_ct_template_version = version.parse(self.sync_load_template_version(template_handle))
        is_major_update, is_minor_update, is_patch_update = False, False, False

        # check if a major change happened (for example 1.2.3 to 2.0.0)
        if template_version_last_sync.major < current_ct_template_version.major:
            is_major_update = True
        # check if minor update happened (for example 1.2.3 to 1.3.0)
        elif template_version_last_sync.minor < current_ct_template_version.minor:
            is_minor_update = True
        # check if a patch update happened (for example 1.2.3 to 1.2.4)
        elif template_version_last_sync.micro < current_ct_template_version.micro:
            is_patch_update = True
        return is_major_update, is_minor_update, is_patch_update, str(template_version_last_sync), str(current_ct_template_version)

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
