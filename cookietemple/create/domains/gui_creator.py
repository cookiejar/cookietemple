import os
import click
from pathlib import Path
from dataclasses import dataclass

from cookietemple.create.template_creator import TemplateCreator
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructGui(CookietempleTemplateStruct):
    """
    This class contains all attributes specific to GUI templates
    """
    id: str = ''
    organization: str = ''


class GuiCreator(TemplateCreator):

    def __init__(self):
        self.gui_struct = TemplateStructGui(domain='gui')
        super().__init__(self.gui_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_GUI_PATH = f'{self.WD_Path.parent}/templates/gui'

        '"" TEMPLATE VERSIONS ""'
        self.GUI_JAVA_TEMPLATE_VERSION = super().load_version('gui-java')

    def create_template(self):
        self.gui_struct.language = click.prompt('Please choose between the following languages [java, kotlin]',
                                                type=click.Choice(['java', 'kotlin']))

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'java': self.gui_java_options,
        }
        switcher.get(self.gui_struct.language.lower(), lambda: 'Invalid language!')()

        # create the gui template
        super().create_template_without_subdomain(self.TEMPLATES_GUI_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            'java': self.GUI_JAVA_TEMPLATE_VERSION,
        }

        self.gui_struct.template_version, self.gui_struct.template_handle = switcher_version.get(
            self.gui_struct.language.lower(), lambda: 'Invalid language!'), f'gui-{self.gui_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations()

    def gui_java_options(self) -> None:
        """
        Prompt the user for all gui-java specific properties
        """
        # The user id is automatically determined from the full_name as first letter of first name and sur name
        full_name_split = self.creator_ctx.full_name.split()
        self.gui_struct.id = f'{full_name_split[0][0]}{full_name_split[1][0]}' if len(full_name_split) > 1 else f'{full_name_split[0][0]}'
        self.gui_struct.organization = click.prompt('Organization:',
                                                    type=str,
                                                    default='cookiejar')
