import os
import click
from pathlib import Path
from dataclasses import dataclass

from cookietemple.create.github_support import prompt_github_repo
from cookietemple.create.template_creator import TemplateCreator
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.custom_cli.questionary import cookietemple_questionary


@dataclass
class TemplateStructCli(CookietempleTemplateStruct):
    """
    CLI-PYTHON
    """
    command_line_interface: str = ''  # which command line library to use (click, argparse)
    testing_library: str = ''  # which testing library to use (pytest, unittest)

    """
    CLI-JAVA
    """
    domain: str = ''  # first part of groupID
    organization: str = ''  # second part of groupID
    main_class: str = ''  # name of the main class (determined from the capital project name)


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

        self.cli_struct.language = cookietemple_questionary('select', 'Choose the project\'s primary language', ['python', 'java', 'kotlin'], 'python')

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': self.cli_python_options,
            'java': self.cli_java_options,
            'kotlin': self.cli_kotlin_options
        }
        switcher.get(self.cli_struct.language)()

        self.cli_struct.is_github_repo, self.cli_struct.is_repo_private, self.cli_struct.is_github_orga, self.cli_struct.github_orga = prompt_github_repo()
        if self.cli_struct.is_github_orga:
            self.cli_struct.github_username = self.cli_struct.github_orga
        # create the chosen and configured template
        super().create_template_without_subdomain(self.TEMPLATES_CLI_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.CLI_PYTHON_TEMPLATE_VERSION,
            'java': self.CLI_JAVA_TEMPLATE_VERSION,
            'kotlin': self.CLI_KOTLIN_TEMPLATE_VERSION
        }
        self.cli_struct.template_version, self.cli_struct.template_handle = switcher_version.get(
            self.cli_struct.language), f'cli-{self.cli_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(domain='cli', language=self.cli_struct.language)

    def cli_python_options(self):
        """ Prompts for cli-python specific options and saves them into the CookietempleTemplateStruct """
        self.cli_struct.command_line_interface = cookietemple_questionary('select', 'Choose a command line library',
                                                                          ['Click', 'Argparse', 'No command-line interface'], 'Click')
        self.cli_struct.testing_library = cookietemple_questionary('select', 'Choose a testing library', ['pytest', 'unittest'], 'pytest')

    def cli_java_options(self) -> None:
        """ Prompts for cli-java specific options and saves them into the CookietempleTemplateStruct """
        self.cli_struct.group_domain = cookietemple_questionary('text', 'Domain (e.g. the org of org.apache)', default='com')
        self.cli_struct.group_organization = cookietemple_questionary('text', 'Organization (e.g. the apache of org.apache)', default='organization')
        self.cli_struct.main_class = self.cli_struct.project_slug.capitalize()

    def cli_kotlin_options(self) -> None:
        """ Prompts for cli-kotlin specific options and saves them into the CookietempleTemplateStruct """
        click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
