import os
from pathlib import Path
from dataclasses import dataclass
import click

from cookietemple.create.template_creator import TemplateCreator
from cookietemple.create.github_support import load_github_username
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.config_command.config import ConfigCommand


@dataclass
class TemplateStructPub(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for PUB projects
    """
    """
    This section contains some PUB-domain specific attributes
    """
    pubtype: str = ''
    author: str = ''
    title: str = ''
    university: str = ''
    department: str = ''
    degree: str = ''
    github_username = ''


class PubCreator(TemplateCreator):

    def __init__(self):
        self.pub_struct = TemplateStructPub(domain='pub', language='latex')
        super().__init__(self.pub_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_PUB_PATH = f'{self.WD_Path.parent}/templates/pub'
        self.CWD = os.getcwd()

        '"" TEMPLATE VERSIONS ""'
        self.PUB_LATEX_TEMPLATE_VERSION = super().load_version('pub-thesis-latex')

    def create_template(self):
        """
        Prompts the user for the publication type and forwards to subsequent prompts.
        Creates the pub template.
        """
        # latex is default language

        self.pub_struct.pubtype = click.prompt('Please choose between the following publication types',
                                               type=click.Choice(['thesis', 'paper']))
        if not os.path.exists(ConfigCommand.CONF_FILE_PATH):
            click.echo(click.style('No cookietemple config file was found! Is this your first time with Cookietemple?\n', fg='red'))
            click.echo(click.style('Lets set your configs for Cookietemple and you are ready to go!\n', fg='blue'))
            ConfigCommand.all_settings()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'latex': self.common_latex_options,
        }
        switcher.get(self.pub_struct.language.lower(), lambda: 'Invalid language!')()

        self.handle_pub_type()

        # create the pub template
        super().create_template_with_subdomain(self.TEMPLATES_PUB_PATH, self.pub_struct.pubtype)

        # switch case statement to fetch the template version
        switcher_version = {
            'latex': self.PUB_LATEX_TEMPLATE_VERSION,
        }

        self.pub_struct.template_version = switcher_version.get(self.pub_struct.language.lower(), lambda: 'Invalid language!')
        self.pub_struct.template_version, self.pub_struct.template_handle = switcher_version.get(
            self.pub_struct.language.lower(), lambda: 'Invalid language!'), f'pub-{self.pub_struct.pubtype}-{self.pub_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting, but skip common_files copying and rst linting
        super().process_common_operations(skip_common_files=True, skip_fix_underline=True,
                                          domain='pub', subdomain=self.pub_struct.pubtype, language=self.pub_struct.language)

    # TODO: IMPLEMENT BELOW
    def handle_pub_type(self) -> None:
        """
        Determine the type of publication and handle it further.
        """

        switcher = {
            'thesis': self.handle_thesis_latex,
            'paper': self.handle_paper_latex
        }
        switcher.get(self.pub_struct.pubtype.lower(), lambda: 'Invalid Pub Project Type!')()

    def handle_thesis_latex(self) -> None:
        self.pub_struct.degree = click.prompt('Degree:',
                                              type=str,
                                              default='PhD')

    def handle_paper_latex(self) -> None:
        pass

    def common_latex_options(self) -> None:
        """
        Prompt the user for common thesis/paper data
        """
        self.pub_struct.author = click.prompt('Author:',
                                              type=str,
                                              default='Homer Simpson')
        self.pub_struct.project_slug = click.prompt('Project Slug:',
                                                    type=str,
                                                    default='Cookietemple_thesis_template')
        self.pub_struct.title = click.prompt('Publication title:',
                                             type=str,
                                             default='On how Springfield exploded')
        self.pub_struct.university = click.prompt('University:',
                                                  type=str,
                                                  default='Homer J. Simpson University')
        self.pub_struct.department = click.prompt('Department:',
                                                  type=str,
                                                  default='Department of nuclear physics')
        self.pub_struct.github_username = load_github_username()  # Required for Github support
