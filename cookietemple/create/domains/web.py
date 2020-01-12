import os
import click
from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration)

from cookiecutter.main import cookiecutter


WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"
TEMPLATES_WEB_PATH = f"{WD}/../templates/web"

"""Web Template Versions"""
WEB_PYTHON_TEMPLATE_VERSION = '0.1.0'


@click.command()
@click.option('--language',
              type=click.Choice(['Python', 'JavaScript', 'Erlang'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_web(language):
    """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.

        :return: The version and handle of the chosen template for the .cookietemple file creation.
    """

    TEMPLATE_STRUCT["language"] = language

    # prompt the user to fetch general template configurations
    prompt_general_template_configuration(standalone_mode=False)

    # switch case statement to prompt the user to fetch template specific configurations
    switcher = {
        'python': web_python_options
    }
    switcher.get(language.lower(), lambda: 'Invalid language!')(standalone_mode=False)

    # create the chosen and configured, template
    #TODO: ONLY TESTS THE FLASK TEMPLATE THEIR (WEBSITE) -> FRAMEWORK DISTINCTION!!!!
    cookiecutter(f"{TEMPLATES_WEB_PATH}/website_{language}",
                 no_input=True,
                 overwrite_if_exists=True,
                 extra_context=TEMPLATE_STRUCT)

    # switch case statement to fetch the template version
    switcher_version = {
        'python': WEB_PYTHON_TEMPLATE_VERSION
    }

    return switcher_version.get(language.lower(), lambda: 'Invalid language!'), f"cli-{language.lower()}"


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
              default=True)
def web_python_options(command_line_interface, pypi_username, use_pytest, use_pypi_deployment_with_travis,
                       add_pyup_badge):
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

