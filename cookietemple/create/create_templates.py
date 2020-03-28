import os
import shutil
import sys
import tempfile
from distutils.dir_util import copy_tree
from shutil import copy2
from pathlib import Path

import click
from ruamel.yaml import YAML
from cookiecutter.main import cookiecutter

from cookietemple.create.create_config import TEMPLATE_STRUCT, COMMON_FILES_PATH
from cookietemple.util.dir_util import delete_dir_tree


def create_dot_cookietemple(TEMPLATE_STRUCT: dict, template_version: str, template_handle: str):
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


def create_template_without_subdomain(domain_path: str, domain: str, language: str) -> None:
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


def create_template_with_subdomain_framework(domain_path: str, subdomain: str, language: str, framework: str) -> None:
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
        directory_exists_warning()

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


def create_common_files() -> None:
    """
    This function creates a temporary directory for common files of all templates and applies cookiecutter on them.
    They are subsequently moved into the directory of the created template.
    """

    dirpath = tempfile.mkdtemp()
    copy_tree(f'{COMMON_FILES_PATH}', dirpath)
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
        path = Path(f'{Path.cwd()}/common_files_util/{f}')
        poss_dir = Path(f"{Path.cwd()}/{TEMPLATE_STRUCT['project_slug']}/{f}")
        is_dir = poss_dir.is_dir()

        if is_dir:
            if not not any(Path(poss_dir).iterdir()):
                copy_into_already_existing_directory(path, poss_dir)

        else:
            if is_dir:
                delete_dir_tree(poss_dir)
            path.replace(f"{Path.cwd()}/{TEMPLATE_STRUCT['project_slug']}/{f}")

    shutil.rmtree(dirpath)


def copy_into_already_existing_directory(common_path, dir: Path) -> None:
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
                copy_into_already_existing_directory(child.resolve(), p)
            else:
                p.mkdir()
                shutil.move(child, p)
        if not child.is_dir():
            copy2(str(child), str(dir))


def directory_exists_warning() -> None:
    """
    Prints warning that a directory already exists and any further action on the directory will overwrite its contents.
    """

    click.echo(click.style('WARNING: ', fg='red')
               + click.style(f"A directory named {TEMPLATE_STRUCT['project_slug']} already exists at", fg='red')
               + click.style(f'{os.getcwd()}', fg='green'))
    click.echo()
    click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
    click.echo()
