import os

import click

from pathlib import Path

from cookietemple.create.domains.common_language_config.python_config import common_python_options

from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration,
                                               create_template_without_subdomain, create_common_files)

WD = os.path.dirname(__file__)
WD_Path = Path(WD)
TEMPLATES_PATH = f'{WD}/../templates'
TEMPLATES_CLI_PATH = f'{WD_Path.parent}/templates/cli'

'"" TEMPLATE VERSIONS ""'
CLI_PYTHON_TEMPLATE_VERSION = '0.1.0'
CLI_JAVA_TEMPLATE_VERSION = '0.1.0'
CLI_KOTLIN_TEMPLATE_VERSION = '0.1.0'
CLI_CPP_TEMPLATE_VERSION = '0.1.0'


def handle_cli():
    """
    Handles the CLI domain. Prompts the user for the language, general and domain specific options.

    :return: The version and handle of the chosen template for the .cookietemple file creation.
    """
    language = click.prompt('Choose between the following languages',
                            type=click.Choice(['Python', 'Java', 'Kotlin', 'C++'], case_sensitive=False))

    TEMPLATE_STRUCT['language'] = language

    # prompt the user to fetch general template configurations
    prompt_general_template_configuration()

    # switch case statement to prompt the user to fetch template specific configurations
    switcher = {
        'python': common_python_options,
        'java': cli_java_options,
        'kotlin': cli_kotlin_options,
        'c++': cli_cpp_options
    }
    switcher.get(language.lower(), lambda: 'Invalid language!')()

    # create the chosen and configured template
    create_template_without_subdomain(f'{TEMPLATES_CLI_PATH}', 'cli', language.lower())

    # create the common files and copy them into the templates directory
    create_common_files()

    # switch case statement to fetch the template version
    switcher_version = {
        'python': CLI_PYTHON_TEMPLATE_VERSION,
        'java': CLI_JAVA_TEMPLATE_VERSION,
        'kotlin': CLI_KOTLIN_TEMPLATE_VERSION,
        'c++': CLI_CPP_TEMPLATE_VERSION
    }

    return switcher_version.get(language.lower(), lambda: 'Invalid language!'), f'cli-{language.lower()}'


def cli_java_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_kotlin_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_cpp_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
