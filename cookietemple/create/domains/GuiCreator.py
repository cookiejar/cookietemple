import os
import click

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.util.template_struct_dataclasses.Template_Struct_GUI import TemplateStructGui as Tsg


class GuiCreator(TemplateCreator):
    """
    TODO: Implement me as soon as any GUI templates are available
    """

    def __init(self):
        self.gui_struct = Tsg(domain='gui')
        super().__init__(self.gui_struct)
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/../templates'  # this may be inherited, review after final setup

    def create_template(self):
        self.gui_struct.language = click.prompt('Please choose between the following languages [c++, c#, java]',
                                                type=click.Choice(['c++', 'c#', 'java']))
        print("NOT IMPLEMENTED YET")
