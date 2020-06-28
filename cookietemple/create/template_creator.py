import os
import sys
import click
import shutil
import re
import tempfile

import requests
from distutils.dir_util import copy_tree
from pathlib import Path
from dataclasses import asdict
from ruamel.yaml import YAML
from cookiecutter.main import cookiecutter

from cookietemple.custom_cli.questionary import cookietemple_questionary
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.github_support import create_push_github_repository, load_github_username, is_git_repo
from cookietemple.lint.lint import lint_project
from cookietemple.util.docs_util import fix_short_title_underline
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.config.config import ConfigCommand
from cookietemple.util.yaml_util import load_yaml_file


class TemplateCreator:
    """
    The base class for all creators.
    It holds the basic template information that are common across all templates (like a project name).
    Furthermore it defines methods that are basic for the template creation process.
    """

    def __init__(self, creator_ctx: CookietempleTemplateStruct):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/templates'
        self.COMMON_FILES_PATH = f'{self.TEMPLATES_PATH}/common_files'
        self.AVAILABLE_TEMPLATES_PATH = f'{self.TEMPLATES_PATH}/available_templates.yml'
        self.AVAILABLE_TEMPLATES = load_yaml_file(self.AVAILABLE_TEMPLATES_PATH)
        self.CWD = os.getcwd()
        self.creator_ctx = creator_ctx

    def process_common_operations(self, skip_common_files=False, skip_fix_underline=False,
                                  domain: str = None, subdomain: str = None, language: str = None) -> None:
        """
        Create all stuff that is common for cookietemples template creation process; in detail those things are:
        create and copy common files, fix docs style, lint the project and ask whether the user wants to create a github repo.
        """
        # create the common files and copy them into the templates directory (skip if flag is set)
        if not skip_common_files:
            self.create_common_files()

        self.create_dot_cookietemple(template_version=self.creator_ctx.template_version)

        project_path = f'{self.CWD}/{self.creator_ctx.project_slug}'

        # Ensure that docs are looking good (skip if flag is set)
        if not skip_fix_underline:
            fix_short_title_underline(f'{project_path}/docs/index.rst')

        # Lint the project to verify that the new template adheres to all standards
        lint_project(project_path, is_create=True)

        if self.creator_ctx.is_github_repo:
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            tmp_project_path = f'{project_path}_cookietemple_tmp'
            os.mkdir(tmp_project_path)
            create_push_github_repository(project_path, self.creator_ctx, tmp_project_path)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

        if subdomain:
            click.echo()
            click.echo(
                click.style(f'Please visit: https://cookietemple.readthedocs.io/en/latest/available_templates.html#{domain}-{subdomain}-{language} '
                            f'for more information about how to use your chosen template.', fg='blue'))
        else:
            click.echo()
            click.echo(
                click.style(f'Please visit: https://cookietemple.readthedocs.io/en/latest/available_templates.html#{domain}-{language} '
                            f'for more information about how to use your chosen template.', fg='blue'))

    def create_template_without_subdomain(self, domain_path: str) -> None:
        """
        Creates a chosen template that does **not** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        """
        # Target directory is already occupied -> overwrite?
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary('confirm', 'Do you really want to continue?', default='Yes'):
                cookiecutter(f'{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())
            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def create_template_with_subdomain(self, domain_path: str, subdomain: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        """
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary('confirm', 'Do you really want to continue?', default='Yes'):
                delete_dir_tree(Path(f'{os.getcwd()}/{self.creator_ctx.project_slug}'))
                cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())

            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def create_template_with_subdomain_framework(self, domain_path: str, subdomain: str, framework: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        :param framework: Chosen framework
        """
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary('confirm', 'Do you really want to continue?', default='Yes'):
                cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=self.creator_ctx_to_dict())

            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=self.creator_ctx_to_dict())

    def prompt_general_template_configuration(self):
        """
        Prompts the user for general options that are required by all templates.
        Options are saved in the creator context manager object.
        """
        try:
            # try to read name and email from existing config file
            self.creator_ctx.full_name = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['full_name']
            self.creator_ctx.email = load_yaml_file(ConfigCommand.CONF_FILE_PATH)['email']
        except FileNotFoundError:
            # style and automatic use config
            click.echo(click.style('Cannot find a cookietemple config file. Is this your first time using cookietemple?', fg='red'))
            # inform the user and config all settings (with PAT optional)
            click.echo(click.style('Lets set your name, email and Github username and you´re ready to go!', fg='blue'))
            ConfigCommand.all_settings()
            # load mail and full name
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML(typ='safe')
            settings = yaml.load(path)
            # set full name and mail
            self.creator_ctx.full_name = settings['full_name']
            self.creator_ctx.email = settings['email']

        self.creator_ctx.project_name = cookietemple_questionary('text', 'Project name', default='Exploding Springfield')

        # check if the project name is already taken on readthedocs.io
        while self.readthedocs_slug_already_exists(self.creator_ctx.project_name):
            click.echo(click.style(f'A project named {self.creator_ctx.project_name} already exists at readthedocs.io!', fg='red'))
            if cookietemple_questionary('confirm', 'Do you want to choose another name for your project?\n'
                                                   'Otherwise you will not be able to host your docs at readthedocs.io!', default='Yes'):
                self.creator_ctx.project_name = cookietemple_questionary('text', 'Project name', default='Exploding Springfield')
            # break if the project should be named anyways
            else:
                break
        self.creator_ctx.project_slug = self.creator_ctx.project_name.replace(' ', '_').replace('-', '_')
        self.creator_ctx.project_short_description = cookietemple_questionary('text', 'Short description of your project',
                                                                              default=f'{self.creator_ctx.project_name}. A cookietemple based .')
        poss_vers = cookietemple_questionary('text', 'Initial version of your project', default='0.1.0')

        # make sure that the version has the right format
        while not re.match(r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)', poss_vers):
            click.echo(click.style('The version number entered does not match cookietemples pattern.\n'
                                   'Please enter the version in the format [number].[number].[number]!', fg='red'))
            poss_vers = cookietemple_questionary('text', 'Initial version of your project', default='0.1.0')
        self.creator_ctx.version = poss_vers

        self.creator_ctx.license = cookietemple_questionary('select', 'License', ['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Boost', 'Affero',
                                                                                  'CC0', 'CCBY', 'CCBYSA', 'Eclipse', 'WTFPL', 'unlicence', 'Not open source'],
                                                            'MIT')

        self.creator_ctx.github_username = load_github_username()

    def create_common_files(self) -> None:
        """
        This function creates a temporary directory for common files of all templates and applies cookiecutter on them.
        They are subsequently moved into the directory of the created template.
        """
        dirpath = tempfile.mkdtemp()
        copy_tree(f'{self.COMMON_FILES_PATH}', dirpath)
        cwd_project = Path.cwd()
        os.chdir(dirpath)
        cookiecutter(dirpath,
                     extra_context={'full_name': self.creator_ctx.full_name,
                                    'email': self.creator_ctx.email,
                                    'language': self.creator_ctx.language,
                                    'domain': self.creator_ctx.domain,
                                    'project_name': self.creator_ctx.project_name,
                                    'project_slug': self.creator_ctx.project_slug,
                                    'version': self.creator_ctx.version,
                                    'license': self.creator_ctx.license,
                                    'project_short_description': self.creator_ctx.project_short_description},
                     no_input=True,
                     overwrite_if_exists=True)

        # recursively copy the common files directory content to the created project
        copy_tree(f'{os.getcwd()}/common_files_util', f'{cwd_project}/{self.creator_ctx.project_slug}')
        # delete the tmp cookiecuttered common files directory
        delete_dir_tree(Path(f'{Path.cwd()}/common_files_util'))
        shutil.rmtree(dirpath, ignore_errors=True)
        # change to recent cwd so lint etc can run properly
        os.chdir(str(cwd_project))

    def readthedocs_slug_already_exists(self, project_name: str) -> bool:
        """
        Test whether there´s already a project with the same name on readthedocs
        :param project_name Name of the project the user wants to create
        """
        click.echo(click.style(f'Looking up {project_name} at readthedocs.io!', fg='blue'))
        try:
            request = requests.get(f'https://{project_name.replace(" ", "")}.readthedocs.io')
            if request.status_code == 200:
                return True
        # catch exceptions when server may be unavailable or the request timed out
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            click.echo(click.style('Cannot check whether name already taken on readthedocs.io because its unreachable at the moment!', fg='red'))
            return False

    def directory_exists_warning(self) -> None:
        """
        If the directory is already a git directory within the same project, print error message and exit.
        Otherwise print a warning that a directory already exists and any further action on the directory will overwrite its contents.
        """
        if is_git_repo(Path(f'{os.getcwd()}/{self.creator_ctx.project_slug}')):
            click.echo(click.style('ERROR: ', fg='red') + click.style(f'A git project named {self.creator_ctx.project_slug} already exists at ', fg='red')
                       + click.style(f'{os.getcwd()}\n', fg='green'))
            click.echo(click.style('Aborting!', fg='red'))
            sys.exit(1)
        else:
            click.echo(click.style('WARNING: ', fg='red') + click.style(f'A directory named {self.creator_ctx.project_slug} already exists at ', fg='red')
                       + click.style(f'{os.getcwd()}\n', fg='blue'))
            click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))

    def create_dot_cookietemple(self, template_version: str):
        """
        Overrides the version with the version of the template.
        Dumps the configuration for the template generation into a .cookietemple yaml file.

        :param template_version: Version of the specific template
        """
        self.creator_ctx.template_version = f'{template_version} # <<COOKIETEMPLE_NO_BUMP>>'
        with open(f'{self.creator_ctx.project_slug}/.cookietemple.yml', 'w') as f:
            yaml = YAML()
            struct_to_dict = self.creator_ctx_to_dict()
            yaml.dump(struct_to_dict, f)

    def creator_ctx_to_dict(self) -> dict:
        """
        Create a dict from the our Template Structure dataclass
        :return: The dict containing all key-value pairs with non empty values
        """
        return {key: val for key, val in asdict(self.creator_ctx).items() if val != ''}

    def load_version(self, handle: str) -> str:
        """
        Load the version of the template specified by the handler

        :param handle: The template handle
        :return: The version number
        """
        parts = handle.split('-')

        if len(parts) == 2:
            return self.AVAILABLE_TEMPLATES[parts[0]][parts[1]]['version']

        elif len(parts) == 3:
            return self.AVAILABLE_TEMPLATES[parts[0]][parts[1]][parts[2]]['version']
