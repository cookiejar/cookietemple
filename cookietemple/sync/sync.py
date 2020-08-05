#!/usr/bin/env python
"""
Synchronise a pipeline TEMPLATE branch with the template.
"""
from distutils.dir_util import copy_tree
import git
import json
import os
import requests
import shutil
import tempfile
from pathlib import Path

from cookietemple.create.github_support import decrypt_pat, load_github_username

from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.create.create import choose_domain
from packaging import version

from cookietemple.common.version import load_project_template_version_and_handle, load_ct_template_version


class SyncException(Exception):
    """Exception raised when there was an error with TEMPLATE branch synchronisation
    """

    pass


class PullRequestException(Exception):
    """Exception raised when there was an error creating a Pull-Request on GitHub.com
    """

    pass


class PipelineSync(object):
    """Object to hold syncing information and results.

    Args:
        pipeline_dir (str): The path to the Nextflow pipeline root directory
        from_branch (str): The branch to use to fetch config vars. If not set, will use current active branch
        make_pr (bool): Set this to `True` to create a GitHub pull-request with the changes
        gh_username (str): GitHub username
        gh_repo (str): GitHub repository name

    Attributes:
        pipeline_dir (str): Path to target pipeline directory
        from_branch (str): Repo branch to use when collecting workflow variables. Default: active branch.
        original_branch (str): Repo branch that was checked out before we started.
        made_changes (bool): Whether making the new template pipeline introduced any changes
        make_pr (bool): Whether to try to automatically make a PR on GitHub.com
        gh_username (str): GitHub username
        gh_repo (str): GitHub repository name
    """

    def __init__(self, pipeline_dir, from_branch=None, make_pr=True, gh_repo=None, gh_username=None, token=None):
        """ Initialise syncing object """

        self.pipeline_dir = os.path.abspath(pipeline_dir)
        self.from_branch = from_branch
        self.original_branch = None
        self.made_changes = False
        self.make_pr = make_pr
        self.gh_pr_returned_data = {}

        self.gh_username = gh_username if gh_username else load_github_username()
        self.gh_repo = gh_repo
        self.token = token if token else decrypt_pat()
        self.dot_cookietemple = self.dot_cookietemple = load_yaml_file(os.path.join(str(self.pipeline_dir), '.cookietemple.yml'))


    def sync(self):
        """ Find workflow attributes, create a new template pipeline on TEMPLATE
        """

        print("Pipeline directory: {}".format(self.pipeline_dir))
        if self.from_branch:
            print("Using branch `{}` to fetch workflow variables".format(self.from_branch))
        if self.make_pr:
            print("Will attempt to automatically create a pull request")

        self.inspect_sync_dir()
        self.get_wf_config()
        self.checkout_template_branch()
        self.delete_template_branch_files()
        self.make_template_pipeline()
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
            print("No changes made to TEMPLATE - sync complete")
        elif not self.make_pr:
            print(
                "Now try to merge the updates in to your pipeline:\n  cd {}\n  git merge TEMPLATE".format(
                    self.pipeline_dir
                )
            )

    def inspect_sync_dir(self):
        """Takes a look at the target directory for syncing. Checks that it's a git repo
        and makes sure that there are no uncommitted changes.
        """
        # Check that the pipeline_dir is a git repo
        try:
            self.repo = git.Repo(self.pipeline_dir)
        except git.exc.InvalidGitRepositoryError as e:
            raise SyncException("'{}' does not appear to be a git repository".format(self.pipeline_dir))

        # get current branch so we can switch back later
        self.original_branch = self.repo.active_branch.name
        print("Original pipeline repository branch is '{}'".format(self.original_branch))

        # Check to see if there are uncommitted changes on current branch
        if self.repo.is_dirty(untracked_files=True):
            raise SyncException(
                "Uncommitted changes found in pipeline directory!\nPlease commit these before running nf-core sync"
            )

    def get_wf_config(self):
        """Check out the target branch if requested and fetch the nextflow config.
        Check that we have the required config variables.
        """
        # Try to check out target branch (eg. `origin/dev`)
        try:
            if self.from_branch and self.repo.active_branch.name != self.from_branch:
                print("Checking out workflow branch '{}'".format(self.from_branch))
                self.repo.git.checkout(self.from_branch)
        except git.exc.GitCommandError:
            raise SyncException("Branch `{}` not found!".format(self.from_branch))

        # If not specified, get the name of the active branch
        if not self.from_branch:
            try:
                self.from_branch = self.repo.active_branch.name
            except git.exc.GitCommandError as e:
                print("Could not find active repo branch: ".format(e))

        # Fetch workflow variables
        print("Fetching workflow config variables")

    def checkout_template_branch(self):
        """
        Try to check out the origin/TEMPLATE in a new TEMPLATE branch.
        If this fails, try to check out an existing local TEMPLATE branch.
        """
        # Try to check out the `TEMPLATE` branch
        try:
            self.repo.git.checkout("origin/TEMPLATE", b="TEMPLATE")
        except git.exc.GitCommandError:
            # Try to check out an existing local branch called TEMPLATE
            try:
                self.repo.git.checkout("TEMPLATE")
            except git.exc.GitCommandError:
                raise SyncException("Could not check out branch 'origin/TEMPLATE' or 'TEMPLATE'")

    def delete_template_branch_files(self):
        """
        Delete all files in the TEMPLATE branch
        """
        # Delete everything
        print("Deleting all files in TEMPLATE branch")
        for the_file in os.listdir(self.pipeline_dir):
            if the_file == ".git":
                continue
            file_path = os.path.join(self.pipeline_dir, the_file)
            print("Deleting {}".format(file_path))
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise SyncException(e)

    def make_template_pipeline(self):
        """
        Delete all files and make a fresh template using the workflow variables
        """
        print("Making a new template pipeline using pipeline variables")
        # dry create run from dot_cookietemple in tmp directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # TODO REFACTOR THIS BY PASSING A PATH PARAM TO CHOOSE DOMAIN WHICH DEFAULTS TO CWD WHEN NOT PASSED (INITIAL CREATE)
            old_cwd = str(Path.cwd())
            os.chdir(tmpdirname)
            choose_domain(domain=None, dot_cookietemple=self.dot_cookietemple)
            os.remove(f'{tmpdirname}/{self.dot_cookietemple["project_slug"]}/.github/workflows/sync_project.yml')
            # copy into the cleaned TEMPLATE branch's project directory
            copy_tree(os.path.join(tmpdirname, self.dot_cookietemple['project_slug']), str(self.pipeline_dir))
            os.chdir(old_cwd)

    def commit_template_changes(self):
        """If we have any changes with the new template files, make a git commit
        """
        # Check that we have something to commit
        if not self.repo.is_dirty(untracked_files=True):
            print("Template contains no changes - no new commit created")
            return False
        # Commit changes
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit("Template update for nf-core/tools version {}".format('1.1.0'))
            self.made_changes = True
            print("Committed changes to TEMPLATE branch")
        except Exception as e:
            raise SyncException("Could not commit changes to TEMPLATE:\n{}".format(e))
        return True

    def push_template_branch(self):
        """If we made any changes, push the TEMPLATE branch to the default remote
        and try to make a PR. If we don't have the auth token, try to figure out a URL
        for the PR and print this to the console.
        """
        print("Pushing TEMPLATE branch to remote: '{}'".format(os.path.basename(self.pipeline_dir)))
        try:
            print(self.pipeline_dir)
            origin = self.repo.remote('origin')
            self.repo.head.ref.set_tracking_branch(origin.refs.TEMPLATE)
            print(self.repo.remotes)
            self.repo.git.push()
        except git.exc.GitCommandError as e:
            raise PullRequestException("Could not push TEMPLATE branch:\n  {}".format(e))

    def make_pull_request(self):
        """Create a pull request to a base branch (default: dev),
        from a head branch (default: TEMPLATE)

        Returns: An instance of class requests.Response
        """
        # Check that we know the github username and repo name
        try:
            assert self.gh_username is not None
        except AssertionError:
            raise PullRequestException("Could not find GitHub username and repo name")

        pr_title = "Important! Template update for nf-core/tools v{}".format('1.1.0')
        pr_body_text = (
            "A new release of the main template in nf-core/tools has just been released. "
            "This automated pull-request attempts to apply the relevant updates to this pipeline.\n\n"
            "Please make sure to merge this pull-request as soon as possible. "
            "Once complete, make a new minor release of your pipeline. "
            "For instructions on how to merge this PR, please see "
            "[https://nf-co.re/developers/sync](https://nf-co.re/developers/sync#merging-automated-prs).\n\n"
            "For more information about this release of [nf-core/tools](https://github.com/nf-core/tools), "
            "please see the [nf-core/tools vrelease page](https://github.com/nf-core/tools/releases/tag/)."
        ).format('1.1.0')

        # Try to update an existing pull-request

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
            url="https://api.github.com/repos/Imipenem/Bertmanbean/pulls",
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
            print('worked')

        # Something went wrong
        else:
            raise PullRequestException(
                "GitHub API returned code {}: \n{}".format(r.status_code, returned_data_prettyprint)
            )

    def reset_target_dir(self):
        """
        Reset the target pipeline directory. Check out the original branch.
        """
        print("Checking out original branch: '{}'".format(self.original_branch))
        try:
            self.repo.git.checkout(self.original_branch)
        except git.exc.GitCommandError as e:
            raise SyncException("Could not reset to original branch `{}`:\n{}".format(self.from_branch, e))

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
