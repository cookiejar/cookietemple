import os
import tempfile
import shutil
from distutils.dir_util import copy_tree

import click
import yaml
from cookiecutter.main import cookiecutter



# The main dictionary, which will be completed by first the general options prompts and then the chosen template
# specific prompts. It is then passed onto cookiecutter as extra_content to facilitate the template creation.
# Finally, it is also used for the creation of the .cookietemple file.
import cookietemple.cookietemple_cli

TEMPLATE_STRUCT = {}

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/templates"
COMMON_FILES_PATH = f"{WD}/templates/common_files"


def prompt_general_template_configuration():
    """
    Prompts the user for general options that are required by all templates.
    Options are saved in the TEMPLACE_STRUCT dict.
    """

    TEMPLATE_STRUCT['full_name'] = click.prompt('Please enter your full name',
                                                type=str,
                                                default='Homer Simpson')
    TEMPLATE_STRUCT['email'] = click.prompt('Please enter your personal or work email',
                                            type=str,
                                            default='homer.simpson@example.com')
    TEMPLATE_STRUCT['github_username'] = click.prompt('Please enter your Github account name',
                                                      type=str,
                                                      default='homersimpson')
    TEMPLATE_STRUCT['project_name'] = click.prompt('Please enter your project name',
                                                   type=str,
                                                   default='Exploding Springfield')
    TEMPLATE_STRUCT['project_slug'] = click.prompt(
        'Please enter an URL friendly project slug. Refrain from using spaces or uncommon letters.',
        type=str,
        default='Exploding-Springfield')
    TEMPLATE_STRUCT['project_short_description'] = click.prompt('Please enter a short description of yor project.',
                                                                type=str,
                                                                default='Exploding Springfield. How to get rid of your job in 3 simple steps.')
    TEMPLATE_STRUCT['version'] = click.prompt('Please enter the initial version of your project.',
                                              type=str,
                                              default='0.1.0')
    TEMPLATE_STRUCT['license'] = click.prompt('Please choose a license',
                                              type=click.Choice(
                                                  ['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Not open source'],
                                                  case_sensitive=False),
                                              show_choices=True,
                                              default='MIT')


def create_dot_cookietemple(TEMPLATE_STRUCT: dict, template_version: str, template_handle: str):
    """
    Overrides the version with the version of the template.
    Dumps the configuration for the template generation into a .cookietemple yaml file.

    :param TEMPLATE_STRUCT: Global variable containing all cookietemple creation configuration variables
    :param template_version: Version of the specific template
    """
    TEMPLATE_STRUCT['template_version'] = template_version
    TEMPLATE_STRUCT['template_handle'] = template_handle
    with open(f'{TEMPLATE_STRUCT["project_slug"]}/.cookietemple', 'w') as f:
        yaml.dump(TEMPLATE_STRUCT, f)


def create_template_without_subdomain(domain_path: str, domain: str, language: str):
    """
    TODO
    :param domain_path:
    :param domain:
    :param language:
    :return:
    """
    proceed = True

    if os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}"):
        click.echo(click.style('WARNING: ', fg='red') + click.style(
            f"A directory named {TEMPLATE_STRUCT['project_slug']} already "
            f"exists at", fg='red') + click.style(f"{os.getcwd()}", fg='green'))
        click.echo()
        click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
        click.echo()
        proceed = click.confirm("Do you really want to continue?")

    if proceed:
        cookiecutter(f"{domain_path}/{domain}_{language}",
                     no_input=True,
                     overwrite_if_exists=True,
                     extra_context=TEMPLATE_STRUCT)

    return proceed


def create_template_with_subdomain_framework(domain_path: str, subdomain: str, language: str, framework: str):
    """
    TODO
    :param domain_path:
    :param subdomain:
    :param language:
    :param framework:
    :return:
    """
    proceed = True

    if os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}"):
        click.echo(click.style('WARNING: ', fg='red') + click.style(
            f"A directory named {TEMPLATE_STRUCT['project_slug']} already "
            f"exists at", fg='red') + click.style(f"{os.getcwd()}", fg='green'))
        click.echo()
        click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
        click.echo()
        proceed = click.confirm("Do you really want to continue?")

    if proceed:
        cookiecutter(f"{domain_path}/{subdomain}_{language}/{framework}",
                     no_input=True,
                     overwrite_if_exists=True,
                     extra_context=TEMPLATE_STRUCT)

    else: click.Context(command=cookietemple.cookietemple_cli.cookietemple_cli).abort()


def cookiecutter_common_files():
    """
    This function creates a temporary directory for common files of all templates and applies cookiecutter on them.

    It´ll be outputted to the created template directory.
    """
    dirpath = tempfile.mkdtemp()
    copy_tree(f"{COMMON_FILES_PATH}", dirpath)
    cookiecutter(dirpath,
                 extra_context={"full_name": TEMPLATE_STRUCT['full_name'],
                                "email": TEMPLATE_STRUCT['email'],
                                "language": TEMPLATE_STRUCT['language'],
                                "project_slug": TEMPLATE_STRUCT['project_slug'],
                                "github_username": TEMPLATE_STRUCT['github_username'],
                                "version": TEMPLATE_STRUCT['version'],
                                "license": TEMPLATE_STRUCT['license'],
                                "project_short_description": TEMPLATE_STRUCT['project_short_description']},
                 no_input=True,
                 overwrite_if_exists=True)

    common_files = os.listdir(f"{os.getcwd()}/common_files_util/")
    for f in common_files:
        shutil.move(os.path.join(f"{os.getcwd()}/common_files_util/", f),
                    os.path.join(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}", f))

    os.removedirs(f"{os.getcwd()}/common_files_util")
    shutil.rmtree(dirpath)
