import os
import sys
import shutil
import re
import tempfile
from distutils.dir_util import copy_tree
from shutil import copy2
from pathlib import Path
from dataclasses import asdict

import click
from ruamel.yaml import YAML
from cookiecutter.main import cookiecutter

from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.github_support import create_push_github_repository, load_github_username
from cookietemple.linting.lint import lint_project
from cookietemple.util.docs_util import fix_short_title_underline
from cookietemple.list.list import load_available_templates
from cookietemple.util.cookietemple_template_struct import CookietempleTemplateStruct


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
        self.AVAILABLE_TEMPLATES = load_available_templates(self.AVAILABLE_TEMPLATES_PATH)
        self.CWD = os.getcwd()
        self.creator_ctx = creator_ctx

    def process_common_operations(self, skip_common_files=False, skip_fix_underline=False) -> None:
        """
        Create all stuff that is common for cookietemples template creation process; in detail those things are:
        create and copy common files, fix docs style, lint the project and ask whether the user wants to create a github repo.
        """
        # create the common files and copy them into the templates directory (skip if flag is set)
        if not skip_common_files:
            self.create_common_files()

        self.create_dot_cookietemple(template_version=self.creator_ctx.template_version)

        project_name = self.creator_ctx.project_slug
        project_path = f'{self.CWD}/{project_name}'

        # Ensure that docs are looking good (skip if flag is set)
        if not skip_fix_underline:
            fix_short_title_underline(f'{project_path}/docs/index.rst')

        # Lint the project to verify that the new template adheres to all standards
        lint_project(project_path, run_coala=False)

        # ask user whether he wants to create a Github repository and do so if specified
        create_github_repository = click.prompt(
            'Do you want to create a Github repository and push your template to it? [y, n]:',
            type=bool,
            default='Yes')
        if create_github_repository:
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            tmp_project_path = f'{project_path}_cookietemple_tmp'
            os.rename(project_path, tmp_project_path)
            create_push_github_repository(project_name, 'some description', tmp_project_path, self.creator_ctx.github_username)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

    def create_template_without_subdomain(self, domain_path: str) -> None:
        """
        Creates a chosen template that does **not** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param domain: Chosen domain
        :param language: Primary chosen language
        """
        # Target directory is already occupied -> overwrite?
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if click.confirm('Do you really want to continue?'):
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
        :param language: Primary chosen language
        """
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if click.confirm('Do you really want to continue?'):
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
        :param language: Primary chosen language
        :param framework: Chosen framework
        """
        occupied = os.path.isdir(f'{os.getcwd()}/{self.creator_ctx.project_slug}')
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if click.confirm('Do you really want to continue?'):
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

        self.creator_ctx.full_name = click.prompt('Please enter your full name',
                                                  type=str,
                                                  default='Homer Simpson')
        self.creator_ctx.email = click.prompt('Please enter your personal or work email',
                                              type=str,
                                              default='homer.simpson@example.com')
        self.creator_ctx.project_name = click.prompt('Please enter your project name',
                                                     type=str,
                                                     default='Exploding Springfield')
        self.creator_ctx.project_slug = self.creator_ctx.project_name.replace(' ', '_')
        self.creator_ctx.project_short_description = click.prompt('Please enter a short description of your project.',
                                                                  type=str,
                                                                  default=f'{self.creator_ctx.project_name}. A best practice .')

        poss_vers = click.prompt('Please enter the initial version of your project.',
                                 type=str,
                                 default='0.1.0')

        # make sure that the version has the right format
        while not re.match(r'[0-9]+\.[0-9]+\.[0-9]+', poss_vers):
            click.echo(click.style('The version number entered does not match cookietemples pattern.\n'
                                   'Please enter the version in the format [number].[number].[number]!', fg='red'))
            poss_vers = click.prompt('Please enter the initial version of your project.',
                                     type=str,
                                     default='0.1.0')

        self.creator_ctx.version = poss_vers

        self.creator_ctx.license = click.prompt(
            'Please choose a license [MIT, BSD, ISC, Apache2.0, GNUv3, Not open source]',
            type=click.Choice(['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Not open source']),
            default='MIT')

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
                                    'project_slug': self.creator_ctx.project_slug,
                                    'version': self.creator_ctx.version,
                                    'license': self.creator_ctx.license,
                                    'project_short_description': self.creator_ctx.project_short_description},
                     no_input=True,
                     overwrite_if_exists=True)

        common_files = os.listdir(f'{os.getcwd()}/common_files_util/')

        for f in common_files:
            path = Path(f'{os.getcwd()}/common_files_util/{f}')
            poss_dir = Path(f'{cwd_project}/{self.creator_ctx.project_slug}/{f}')
            is_dir = poss_dir.is_dir()

            # if directory already exists add the missing files
            if is_dir:
                if any(Path(poss_dir).iterdir()):
                    self.copy_into_already_existing_directory(path, poss_dir)

            else:
                # if its a directory delete it and copy new content
                if is_dir:
                    delete_dir_tree(poss_dir)
                shutil.copy(path, f'{cwd_project}/{self.creator_ctx.project_slug}/{f}')
                os.remove(path)

        delete_dir_tree(Path(f'{Path.cwd()}/common_files_util'))
        shutil.rmtree(dirpath)
        os.chdir(str(cwd_project))

    def copy_into_already_existing_directory(self, common_path, dir: Path) -> None:
        """
        This function copies all files of an arbitrarily deep nested directory that is already on the main directory
        and just adds them where they belong.

        :param common_path: Path where the common files are located
        :param dir: The projects directory where collisions occurred (co-existence)
        """
        for child in common_path.iterdir():
            if child.is_dir():
                p = Path(f'{dir}/{child.name}')
                if p.exists():
                    self.copy_into_already_existing_directory(child.resolve(), p)
                else:
                    shutil.copytree(str(child), str(p))
            if not child.is_dir():
                copy2(str(child), str(dir))

    def directory_exists_warning(self) -> None:
        """
        Prints warning that a directory already exists and any further action on the directory will overwrite its contents.
        """

        click.echo(click.style('WARNING: ', fg='red')
                   + click.style(f'A directory named {self.creator_ctx.project_slug} already exists at', fg='red')
                   + click.style(f'{os.getcwd()}', fg='green'))
        click.echo()
        click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
        click.echo()

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
        TODO: Maybe recursive one for arbitray length (tough I Dont think we will need it)
        :param handle: The template handle
        :return: The version number
        """
        parts = handle.split('-')

        if len(parts) == 2:
            return self.AVAILABLE_TEMPLATES[parts[0]][parts[1]]['version']

        elif len(parts) == 3:
            return self.AVAILABLE_TEMPLATES[parts[0]][parts[1]][parts[2]]['version']
