import os
import click
from pathlib import Path

from cookietemple.create.domains.common_language_config.python_config import common_python_options
from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.util.template_struct_dataclasses.Template_Struct_CLI import TemplateStructCli as Tsc


class CliCreator(TemplateCreator):

    def __init__(self):
        self.cli_struct = Tsc(domain='cli')
        super().__init__(self.cli_struct)
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
        """

        self.cli_struct.language = click.prompt('Choose between the following languages [python, java, kotlin, c++]',
                                                type=click.Choice(['python', 'java', 'kotlin', 'c++'])).capitalize()

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': common_python_options,
            'java': cli_java_options,
            'kotlin': cli_kotlin_options,
            'c++': cli_cpp_options
        }
        switcher.get(self.cli_struct.language.lower(), lambda: 'Invalid language!')(self.creator_ctx)

        # create the chosen and configured template
        super().create_template_without_subdomain(f'{self.TEMPLATES_CLI_PATH}')

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.CLI_PYTHON_TEMPLATE_VERSION,
            'java': self.CLI_JAVA_TEMPLATE_VERSION,
            'kotlin': self.CLI_KOTLIN_TEMPLATE_VERSION,
            'c++': self.CLI_CPP_TEMPLATE_VERSION
        }
        self.cli_struct.template_version, self.cli_struct.template_handle = switcher_version.get(
            self.cli_struct.language.lower(), lambda: 'Invalid language!'), f'cli-{self.cli_struct.language.lower()}'

        super().create_common()


def cli_java_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_kotlin_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))


def cli_cpp_options():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
