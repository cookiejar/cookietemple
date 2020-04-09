import os
import click
from pathlib import Path

from cookietemple.create.domains.common_language_config.python_config import common_python_options
from cookietemple.create.create_config import TEMPLATE_STRUCT
from cookietemple.create.TemplateCreator import TemplateCreator


class CliCreator(TemplateCreator):

    def __init__(self):
        super().__init__()
        self.WD = os.path.dirname(__file__)
        self.WD_Path = Path(self.WD)
        self.TEMPLATES_PATH = f'{self.WD}/../templates'  # this may be inherited, review after final setup
        self.TEMPLATES_CLI_PATH = f'{self.WD_Path.parent}/templates/cli'

        '"" TEMPLATE VERSIONS ""'
        self.CLI_PYTHON_TEMPLATE_VERSION = '0.1.0'
        self.CLI_JAVA_TEMPLATE_VERSION = '0.1.0'
        self.CLI_KOTLIN_TEMPLATE_VERSION = '0.1.0'
        self.CLI_CPP_TEMPLATE_VERSION = '0.1.0'

    def create_template(self):
        """
        Handles the CLI domain. Prompts the user for the language, general and domain specific options.

        :return: The version and handle of the chosen template for the .cookietemple file creation.
        """

        language = click.prompt('Choose between the following languages [python, java, kotlin, c++]',
                                type=click.Choice(['python', 'java', 'kotlin', 'c++']))

        TEMPLATE_STRUCT['language'] = language.capitalize()

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': common_python_options,
            'java': cli_java_options,
            'kotlin': cli_kotlin_options,
            'c++': cli_cpp_options
        }
        switcher.get(language.lower(), lambda: 'Invalid language!')()

        # create the chosen and configured template
        super().create_template_without_subdomain(f'{self.TEMPLATES_CLI_PATH}', 'cli', language.lower())

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.CLI_PYTHON_TEMPLATE_VERSION,
            'java': self.CLI_JAVA_TEMPLATE_VERSION,
            'kotlin': self.CLI_KOTLIN_TEMPLATE_VERSION,
            'c++': self.CLI_CPP_TEMPLATE_VERSION
        }
        template_version, template_handle = switcher_version.get(language.lower(), lambda: 'Invalid language!'), f'cli-{language.lower()}'
        super().create_common(template_version, template_handle)


def cli_java_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_kotlin_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_cpp_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
