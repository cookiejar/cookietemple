import os
import shutil
import git
import tempfile
from distutils.dir_util import copy_tree
from pathlib import Path
from packaging import version
from rich import print

from cookietemple.common.version import load_ct_template_version, load_project_template_version_and_handle
from cookietemple.create.github_support import load_github_username, decrypt_pat
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.create.create import choose_domain


class Sync:
    """
    Sync class that wraps all functionality for cookietemple's syncing feature
    """

    def __init__(self, pat, project_dir: Path):
        self.project_dir = project_dir
        self.github_username = load_github_username()
        self.pat = pat if pat else decrypt_pat()
        self.dot_cookietemple = {}

    def sync(self):
        """
        Sync main function that calls the various steps included in a sync process.
        :return:
        """
        # check necessary conditions a project must met in order to run sync
        self.inspect_sync_dir()
        self.checkout_template_branch()
        self.clean_template_branch()
        self.create_new_template()

    def checkout_template_branch(self) -> None:
        """
        Checkout to the TEMPLATE branch (if available).
        If this fails, create a new branch called TEMPLATE and proceed.
        """
        # Try to check out the local TEMPLATE branch
        try:
            self.repo.git.checkout('TEMPLATE')
        except git.exc.GitCommandError:
            # Try to check out a remote branch called TEMPLATE
            try:
                self.repo.git.checkout('origin/TEMPLATE', b='TEMPLATE')
            except git.exc.GitCommandError:
                print('[bold blue] Could not checkout to TEMPLATE branch. Creating new branch called TEMPLATE!')
                self.repo.git.checkout('-b', 'TEMPLATE')

    def clean_template_branch(self) -> None:
        """
        Remove everything on the local TEMPLATE branch to provide a clean base for the creation of the newest template.
        """

        # Delete everything
        print('[bold blue]Deleting all files in TEMPLATE branch')
        for the_file in os.listdir(str(self.project_dir)):
            # keep the .git directory
            if the_file == '.git':
                continue
            file_path = os.path.join(str(self.project_dir), the_file)
            # clean TEMPLATE branch locally
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'[bold red]{e}')

    def create_new_template(self):
        """
        Create a new template using the content of the .cookietemple.yml file from the old TEMPLATE branch to obtain the TEMPLATE branch
        with the newest cookietemple raw template.
        """
        # dry create run from dot_cookietemple in tmp directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # TODO REFACTOR THIS BY PASSING A PATH PARAM TO CHOOSE DOMAIN WHICH DEFAULTS TO CWD WHEN NOT PASSED (INITIAL CREATE)
            old_cwd = str(Path.cwd())
            os.chdir(tmpdirname)
            choose_domain(domain=None, dot_cookietemple=self.dot_cookietemple)
            # copy into the cleaned TEMPLATE branch's project directory
            copy_tree(os.path.join(tmpdirname, self.dot_cookietemple['project_slug']), str(self.project_dir))
            os.chdir(old_cwd)

    def create_pull_request(self):
        pass

    def checkout_original_branch(self):
        pass

    def inspect_sync_dir(self):
        """
        Takes a look at the target directory for syncing. Checks that it's a git repo, makes sure that there are no uncommitted changes and checks, if a
        .cookietemple.yml file exists!
        """
        # check that the project_dir contains a .cookietemple.yml file
        if not os.path.exists(os.path.join(str(self.project_dir), '.cookietemple.yml')):
            raise Exception(f'{self.project_dir} does not appear to contain a .cookietemple.yml file. Did you delete it?')
        # store .cookietemple.yml content for later reuse in the dry create run
        self.dot_cookietemple = load_yaml_file(os.path.join(str(self.project_dir), '.cookietemple.yml'))
        try:
            self.repo = git.Repo(self.project_dir)
        except git.exc.InvalidGitRepositoryError:
            raise Exception(f'{self.project_dir} does not appear to be a git repository')

        # get current branch so we can switch back later
        self.original_branch = self.repo.active_branch.name
        print(f'Original project repository branch is {self.original_branch}')

        # Check to see if there are uncommitted changes on current branch
        if self.repo.is_dirty(untracked_files=True):
            raise Exception('Uncommitted changes found in project directory!\nPlease commit these before running cookietemple sync')

    def has_template_version_changed(self, project_dir: Path) -> (bool, bool, str, str):
        """
        Check, if the cookietemple template has been updated since last check/sync of the user.

        :return: Both false if no versions changed or a micro change happened (for ex. 1.2.3 to 1.2.4). Return pr_major_change True if a major version release
        happened for the cookietemple template (for example 1.2.3 to 2.0.0). Return issue_minor_change True if a minor change happened (1.2.3 to 1.3.0).
        cookietemple will use this to decide which syncing strategy to apply. Also return both versions.
        """
        template_version_last_sync, template_handle = self.sync_load_project_template_version_and_handle(project_dir)
        template_version_last_sync = version.parse(template_version_last_sync)
        current_ct_template_version = version.parse(self.sync_load_template_version(template_handle))
        # check if a major change happened (for example 1.2.3 to 2.0.0)
        is_version_outdated = True if template_version_last_sync.major < current_ct_template_version.major or \
                                      template_version_last_sync.minor < current_ct_template_version.minor else False
        return is_version_outdated, str(template_version_last_sync), str(current_ct_template_version)

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
