import os
import click
from dataclasses import dataclass

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructGui(CookietempleTemplateStruct):
    """
    This class contains all attributes specific to GUI templates
    """
    pass


class GuiCreator(TemplateCreator):
    """
    TODO: Implement me as soon as any GUI templates are available
    """

    def __init(self):
        self.gui_struct = TemplateStructGui(domain='gui')
        super().__init__(self.gui_struct)
        self.WD = os.path.dirname(__file__)

    def create_template(self):
        self.gui_struct.language = click.prompt('Please choose between the following languages [c++, c#, java]',
                                                type=click.Choice(['c++', 'c#', 'java']))
        print('NOT IMPLEMENTED YET')
