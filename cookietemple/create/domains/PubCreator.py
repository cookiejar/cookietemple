import os
import shutil
from pathlib import Path

import click

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.util.template_struct_dataclasses.Template_Struct_PUB import TemplateStructPub as Tsp
from cookietemple.create.github_support import create_push_github_repository
from cookietemple.linting.lint import lint_project


class PubCreator(TemplateCreator):

    def __init__(self):
        self.pub_struct = Tsp(domain='pub', language='latex')
        super().__init__(self.pub_struct)
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

        self.pub_struct.pubtype = click.prompt('Please choose between the following publication types [thesis, paper]',
                                               type=click.Choice(['thesis', 'paper']))

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'latex': self.common_latex_options,
        }
        switcher.get(self.pub_struct.language.lower(), lambda: 'Invalid language!')()

        self.handle_pub_type()

        super().create_template_with_subdomain(self.TEMPLATES_PUB_PATH, self.pub_struct.pubtype)

        # switch case statement to fetch the template version
        switcher_version = {
            'latex': self.PUB_LATEX_TEMPLATE_VERSION,
        }

        # TODO: REFACTOR THIS, MAYBE DIFFERENCIATE IN TEMPLATECREATOR!
        # WE DONT NEED COMMON FILES AND SHORT UNDERLINES FIX HERE!
        self.pub_struct.template_version = switcher_version.get(self.pub_struct.language.lower(), lambda: 'Invalid language!')
        self.pub_struct.template_version, self.pub_struct.template_handle = switcher_version.get(self.pub_struct.language.lower(), lambda: 'Invalid language!') \
            , f"pub-{self.pub_struct.pubtype}-{self.pub_struct.language.lower()}"
        self.create_dot_cookietemple(self.pub_struct.template_version)

        project_name = self.pub_struct.project_slug
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
