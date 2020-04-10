import os
import shutil
from pathlib import Path

import click

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.create_config import TEMPLATE_STRUCT
from cookietemple.create.github_support import create_push_github_repository
from cookietemple.linting.lint import lint_project


class PubCreator(TemplateCreator):

    def __init__(self):
        super().__init__()
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_PATH = f'{self.WD_Path}/../templates'
        self.TEMPLATES_PUB_PATH = f'{self.WD_Path.parent}/templates/pub'
        self.CWD = os.getcwd()

        '"" TEMPLATE VERSIONS ""'
        self.PUB_LATEX_TEMPLATE_VERSION = '0.1.0'

    def create_template(self):
        """
        Prompts the user for the publication type and forwards to subsequent prompts.
        Creates the pub template.
        """

        # Set latex as default
        language = 'latex'
        TEMPLATE_STRUCT['language'] = language

        TEMPLATE_STRUCT['pubtype'] = click.prompt('Please choose between the following publication types [thesis, paper]',
                                                  type=click.Choice(['thesis', 'paper']))

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'latex': self.common_latex_options,
        }
        switcher.get(language.lower(), lambda: 'Invalid language!')()

        self.handle_pub_type()

        super().create_template_with_subdomain(self.TEMPLATES_PUB_PATH, TEMPLATE_STRUCT['pubtype'],
                                               TEMPLATE_STRUCT['language'].lower())

        # switch case statement to fetch the template version
        switcher_version = {
            'latex': self.PUB_LATEX_TEMPLATE_VERSION,
        }

        # TODO: REFACTOR THIS, MAYBE DIFFERENCIATE IN TEMPLATECREATOR!
        # WE DONT NEED COMMON FILES AND SHORT UNDERLINES FIX HERE!
        template_version, template_handle = switcher_version.get(language.lower(), lambda: 'Invalid language!'), f"pub-{TEMPLATE_STRUCT['pubtype']}-{language.lower()}"
        self.create_dot_cookietemple(TEMPLATE_STRUCT, template_version=template_version, template_handle=template_handle)

        project_name = TEMPLATE_STRUCT['project_slug']
        project_path = f'{self.CWD}/{project_name}'

        # Lint the project to verify that the new template adheres to all standards
        lint_project(project_path, run_coala=False)

        # ask user whether he wants to create a Github repository and do so if specified
        create_github_repository = click.prompt(
            'Do you want to create a Github repository and push your template to it? [y, n]:',
            type=bool,
            default='Yes')
        if create_github_repository:
            tmp_project_path = f'{project_path}_cookietemple_tmp'
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            os.rename(project_path, tmp_project_path)
            create_push_github_repository(project_name, 'some description', tmp_project_path)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

    # TODO: IMPLEMENT BELOW
    def handle_pub_type(self) -> None:
        """
        Determine the type of publication and handle it further.
        """

        switcher = {
            'thesis': self.handle_thesis_latex,
            'paper': self.handle_paper_latex
        }
        switcher.get(TEMPLATE_STRUCT['pubtype'].lower(), lambda: 'Invalid Pub Project Type!')()

    def handle_thesis_latex(self) -> None:
        TEMPLATE_STRUCT['degree'] = click.prompt('Degree:',
                                                 type=str,
                                                 default='PhD')

    def handle_paper_latex(self) -> None:
        pass

    def common_latex_options(self) -> None:
        """
        Prompt the user for common thesis/paper data
        """
        TEMPLATE_STRUCT['author'] = click.prompt('Author:',
                                                 type=str,
                                                 default='Homer Simpson')
        TEMPLATE_STRUCT['project_slug'] = click.prompt('Project Slug:',
                                                       type=str,
                                                       default='Cookietemple_thesis_template')
        TEMPLATE_STRUCT['title'] = click.prompt('Publication title:',
                                                type=str,
                                                default='On how Springfield exploded')
        TEMPLATE_STRUCT['university'] = click.prompt('University:',
                                                     type=str,
                                                     default='Homer J. Simpson University')
        TEMPLATE_STRUCT['department'] = click.prompt('Department:',
                                                     type=str,
                                                     default='Department of nuclear physics')
