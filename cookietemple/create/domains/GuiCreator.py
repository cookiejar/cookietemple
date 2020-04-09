import os
import click

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.create_config import TEMPLATE_STRUCT


class GuiCreator(TemplateCreator):
    """
    TODO: Implement me as soon as any GUI templates are available
    """

    def __init(self):
        super().__init__()
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f'{self.WD}/../templates'  # this may be inherited, review after final setup

    def create_template(self):
        language = click.prompt('Please choose between the following languages [c++, c#, java]',
                                type=click.Choice(['c++', 'c#', 'java']))
        TEMPLATE_STRUCT['language'] = language
        print("NOT IMPLEMENTED YET")
