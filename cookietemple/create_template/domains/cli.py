import os
import sys

import click

from cookietemple.create_template.create_config import (TEMPLATE_STRUCT, create_dot_cookietemple)

from cookiecutter.main import cookiecutter

from cookietemple.create_template.create_general_options import determine_general_options

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['python', 'c++', 'kotlin'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_cli(language):
    TEMPLATE_STRUCT["language"] = language

    try:
        determine_general_options()
    except SystemExit as e:
        if e != 0:
            try:
                cli_options()
            except SystemExit as e:
                cookiecutter(f"{TEMPLATES_PATH}/cli_python", no_input=True, overwrite_if_exists=True,
                             extra_context=TEMPLATE_STRUCT)

                create_dot_cookietemple(TEMPLATE_STRUCT)


"""
In the following sub questions we will answer the questions that were previously defined in a cookiecutter.json
{
  "full_name": "Homer Simpson",
  "email": "homer.simpson@example.com",
  "github_username": "homersimpson",
  "project_name": "Python CLI",
  "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
  "project_short_description": "Python CLI contains all the boilerplate you need to create a Python package with commandline support.",
  "pypi_username": "{{ cookiecutter.github_username }}",
  "version": "0.1.0",
  "use_pytest": "y",
  "use_pypi_deployment_with_travis": "y",
  "add_pyup_badge": "n",
  "command_line_interface": ["Click", "Argparse", "No command-line interface"],
  "create_author_file": "y",
  "open_source_license": ["MIT license", "BSD license", "ISC license", "Apache Software License 2.0", "GNU General Public License v3", "Not open source"]
}
"""


@click.command()
@click.option('--command_line_interface',
              type=click.Choice(['Click', 'Argparse', 'No command-line interface'], case_sensitive=False),
              help='Choose which command line library (if any) you want to use. We highly recommend click.',
              prompt='Please choose a command line library.',
              default='Click')
@click.option('--pypi_username',
              type=str,
              help='Your username for pypi. Pypi is commonly used to share your project with the world. If you do not have a pypi username yet you can create one now or do so later.',
              prompt='Please enter your pypi username.',
              default='homersimpson')
@click.option('--use_pytest/--no_pytest',
              help='Pytest is a slightly more advanced testing library. Choose whether you want to work with pytest or unittest',
              prompt='Please choose whether pytest or unittest should be used as the testing library.',
              default=True)
@click.option('--use_pypi_deployment_with_travis/--no_pypi_deployment_with_travis',
              help='Determine whether or not you want boiler plate code for the automatic deployment of your package to pypi via travis.',
              prompt='Please choose whether or not to automatically deploy your project on pypi via travis',
              default=True)
@click.option('--add_pyup_badge/--no_pyup_badge',
              help='pyup is a service that submits pull requests to your repository if any new versions of dependencies have been released. A badge may be added to your README.',
              prompt='Please choose whether or not to include a pyup badge into your README.',
              default='true')
def cli_options(command_line_interface, pypi_username, use_pytest, use_pypi_deployment_with_travis, add_pyup_badge):
    TEMPLATE_STRUCT['command_line_interface'] = command_line_interface
    TEMPLATE_STRUCT['pypi_username'] = pypi_username

    if use_pytest:
        TEMPLATE_STRUCT['use_pytest'] = 'y'
    else:
        TEMPLATE_STRUCT['use_pytest'] = 'n'

    if use_pypi_deployment_with_travis:
        TEMPLATE_STRUCT['use_pypi_deployment_with_travis'] = 'y'
    else:
        TEMPLATE_STRUCT['use_pypi_deployment_with_travis'] = 'n'

    if add_pyup_badge:
        TEMPLATE_STRUCT['add_pyup_badge'] = 'y'
    else:
        TEMPLATE_STRUCT['add_pyup_badge'] = 'n'

    sys.exit()
