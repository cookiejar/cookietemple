import os
import sys
import shutil
import re
import tempfile
from distutils.dir_util import copy_tree
from shutil import copy2
from pathlib import Path
import click
from ruamel.yaml import YAML
from cookiecutter.main import cookiecutter

from cookietemple.create.create_config import TEMPLATE_STRUCT
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.github_support import create_push_github_repository
from cookietemple.linting.lint import lint_project
from cookietemple.util.docs_util import fix_short_title_underline


class TemplateCreator:
    """
    The base class for all creators.
    It holds the basic template information that are common across all templates (like a project name).
    Furthermore it defines methods that are basic for the template creation process.
    """

    def __init__(self):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/templates'
        self.COMMON_FILES_PATH = f'{self.WD}/templates/common_files'
        self.CWD = os.getcwd()

    def create_common(self, template_version, template_handle) -> None:
        """
        Create all stuff that is common for cookietemples template creation process; in detail those things are:
        create and copy common files, fix docs style, lint the project and ask whether the user wants to create a github repo.
        """
        # create the common files and copy them into the templates directory
        self.create_common_files()

        self.create_dot_cookietemple(TEMPLATE_STRUCT, template_version=template_version, template_handle=template_handle)

        project_name = TEMPLATE_STRUCT['project_slug']
        project_path = f'{self.CWD}/{project_name}'

        # Ensure that docs are looking good
        fix_short_title_underline(f'{project_path}/docs/index.rst')

        # Lint the project to verify that the new template adheres to all standards

        lint_project(project_path, run_coala=False)

        # ask user whether he wants to create a Github repository and do so if specified
        create_github_repository = click.prompt(
            'Do you want to create a Github repository and push your template to it? [y, n]:',
            type=bool,
            default='Yes')
        if create_github_repository:
            tmp_project_path = f'{project_path}_cookietemple_tmp'
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            os.rename(project_path, tmp_project_path)
            create_push_github_repository(project_name, 'some description', tmp_project_path)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

    def create_template_without_subdomain(self, domain_path: str, domain: str, language: str) -> None:
        """
        Creates a chosen template that does **not** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param domain: Chosen domain
        :param language: Primary chosen language
        """
        # Target directory is already occupied -> overwrite?
        occupied = os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
        if occupied:
            click.echo(click.style('WARNING: ', fg='red')
                       + click.style(f"A directory named {TEMPLATE_STRUCT['project_slug']} already exists at", fg='red')
                       + click.style(f'{os.getcwd()}', fg='green'))
            click.echo()
            click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
            click.echo()

            if click.confirm('Do you really want to continue?'):
                cookiecutter(f'{domain_path}/{domain}_{language}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=TEMPLATE_STRUCT)
            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{domain}_{language}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=TEMPLATE_STRUCT)

    def create_template_with_subdomain(self, domain_path: str, subdomain: str, language: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        :param language: Primary chosen language
        """
        occupied = os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
        if occupied:
            self.directory_exists_warning()

            if click.confirm('Do you really want to continue?'):
                cookiecutter(f'{domain_path}/{subdomain}_{language}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=TEMPLATE_STRUCT)

            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{language}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=TEMPLATE_STRUCT)

    def create_template_with_subdomain_framework(self, domain_path: str, subdomain: str, language: str, framework: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        :param language: Primary chosen language
        :param framework: Chosen framework
        """
        occupied = os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
        if occupied:
            self.directory_exists_warning()

            if click.confirm('Do you really want to continue?'):
                cookiecutter(f'{domain_path}/{subdomain}_{language}/{framework}',
                             no_input=True,
                             overwrite_if_exists=True,
                             extra_context=TEMPLATE_STRUCT)

            else:
                click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
                sys.exit(0)
        else:
            cookiecutter(f'{domain_path}/{subdomain}_{language}/{framework}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=TEMPLATE_STRUCT)

    def prompt_general_template_configuration(self):
        """
        Prompts the user for general options that are required by all templates.
        Options are saved in the TEMPLATE_STRUCT dict.
        """

        TEMPLATE_STRUCT['full_name'] = click.prompt('Please enter your full name',
                                                    type=str,
                                                    default='Homer Simpson')
        TEMPLATE_STRUCT['email'] = click.prompt('Please enter your personal or work email',
                                                type=str,
                                                default='homer.simpson@example.com')
        TEMPLATE_STRUCT['project_name'] = click.prompt('Please enter your project name',
                                                       type=str,
                                                       default='Exploding Springfield')
        TEMPLATE_STRUCT['project_slug'] = TEMPLATE_STRUCT['project_name'].replace(' ', '_')
        TEMPLATE_STRUCT['project_short_description'] = click.prompt('Please enter a short description of your project.',
                                                                    type=str,
                                                                    default=f'{TEMPLATE_STRUCT["project_name"]}. A best practice .')

        poss_vers = click.prompt('Please enter the initial version of your project.',
                                 type=str,
                                 default='0.1.0')

        while not re.match(r'[0-9]+.[0-9]+.[0-9]+', poss_vers):
            click.echo(click.style('The version number entered does not match cookietemples pattern.\n'
                                   'Please enter the version in the format [number].[number].[number]!', fg='red'))
            poss_vers = click.prompt('Please enter the initial version of your project.',
                                     type=str,
                                     default='0.1.0')

        TEMPLATE_STRUCT['version'] = poss_vers

        TEMPLATE_STRUCT['license'] = click.prompt(
            'Please choose a license [MIT, BSD, ISC, Apache2.0, GNUv3, Not open source]',
            type=click.Choice(['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Not open source']),
            default='MIT')

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
                     extra_context={'full_name': TEMPLATE_STRUCT['full_name'],
                                    'email': TEMPLATE_STRUCT['email'],
                                    'language': TEMPLATE_STRUCT['language'],
                                    'project_slug': TEMPLATE_STRUCT['project_slug'],
                                    'version': TEMPLATE_STRUCT['version'],
                                    'license': TEMPLATE_STRUCT['license'],
                                    'project_short_description': TEMPLATE_STRUCT['project_short_description']},
                     no_input=True,
                     overwrite_if_exists=True)

        common_files = os.listdir(f'{os.getcwd()}/common_files_util/')

        for f in common_files:
            path = Path(f'{os.getcwd()}/common_files_util/{f}')
            poss_dir = Path(f"{cwd_project}/{TEMPLATE_STRUCT['project_slug']}/{f}")
            is_dir = poss_dir.is_dir()

            if is_dir:
                if not not any(Path(poss_dir).iterdir()):
                    self.copy_into_already_existing_directory(path, poss_dir)

            else:
                if is_dir:
                    delete_dir_tree(poss_dir)
                shutil.copy(path, f"{cwd_project}/{TEMPLATE_STRUCT['project_slug']}/{f}")
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
                   + click.style(f"A directory named {TEMPLATE_STRUCT['project_slug']} already exists at", fg='red')
                   + click.style(f'{os.getcwd()}', fg='green'))
        click.echo()
        click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
        click.echo()

    def create_dot_cookietemple(self, TEMPLATE_STRUCT: dict, template_version: str, template_handle: str):
        """
        Overrides the version with the version of the template.
        Dumps the configuration for the template generation into a .cookietemple yaml file.

        :param TEMPLATE_STRUCT: Global variable containing all cookietemple creation configuration variables
        :param template_version: Version of the specific template
        """
        TEMPLATE_STRUCT['template_version'] = f'{template_version} # <<COOKIETEMPLE_NO_BUMP>>'
        TEMPLATE_STRUCT['template_handle'] = template_handle
        with open(f'{TEMPLATE_STRUCT["project_slug"]}/.cookietemple.yml', 'w') as f:
            yaml = YAML()
            yaml.dump(TEMPLATE_STRUCT, f)
