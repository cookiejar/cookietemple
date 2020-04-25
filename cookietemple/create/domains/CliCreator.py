import os
import click
from pathlib import Path
from dataclasses import dataclass

from cookietemple.create.domains.common_language_config.python_config import common_python_options
from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructCli(CookietempleTemplateStruct):
    """
    We dont have any attributes here right now (WIP)
    Intended Use: This class holds all attributes specific for CLI projects
    """
    pass


class CliCreator(TemplateCreator):

    def __init__(self):
        self.cli_struct = TemplateStructCli(domain='cli')
        super().__init__(self.cli_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_CLI_PATH = f'{self.WD_Path.parent}/templates/cli'

        '"" TEMPLATE VERSIONS ""'
        self.CLI_PYTHON_TEMPLATE_VERSION = super().load_version('cli-python')
        self.CLI_JAVA_TEMPLATE_VERSION = super().load_version('cli-java')
        self.CLI_KOTLIN_TEMPLATE_VERSION = super().load_version('cli-kotlin')

    def create_template(self):
        """
        Handles the CLI domain. Prompts the user for the language, general and domain specific options.
        """

        self.cli_struct.language = click.prompt('Choose between the following languages [python, java, kotlin]',
                                                type=click.Choice(['python', 'java', 'kotlin'])).capitalize()

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': common_python_options,
            'java': cli_java_options,
            'kotlin': cli_kotlin_options
        }
        switcher.get(self.cli_struct.language.lower(), lambda: 'Invalid language!')(self.creator_ctx)

        # create the chosen and configured template
        super().create_template_without_subdomain(f'{self.TEMPLATES_CLI_PATH}')

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.CLI_PYTHON_TEMPLATE_VERSION,
            'java': self.CLI_JAVA_TEMPLATE_VERSION,
            'kotlin': self.CLI_KOTLIN_TEMPLATE_VERSION
        }
        self.cli_struct.template_version, self.cli_struct.template_handle = switcher_version.get(
            self.cli_struct.language.lower(), lambda: 'Invalid language!'), f'cli-{self.cli_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations()


def cli_java_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_kotlin_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
