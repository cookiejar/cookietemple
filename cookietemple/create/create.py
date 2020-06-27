import click
import questionary

from cookietemple.create.domains.cli_creator import CliCreator
from cookietemple.create.domains.web_creator import WebCreator
from cookietemple.create.domains.gui_creator import GuiCreator
from cookietemple.create.domains.pub_creator import PubCreator
from cookietemple.custom_cli.questionary_style import cookietemple_style


def choose_domain(domain: str):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    """
    if not domain:
        domain = questionary.select(
            'Choose the project\'s domain',
            choices=[
                'cli',
                'gui',
                'web',
                'pub'
            ], style=cookietemple_style).ask()

    switcher = {
        'cli': CliCreator,
        'web': WebCreator,
        'gui': GuiCreator,
        'pub': PubCreator
    }

    creator_obj = switcher.get(domain.lower())()
    creator_obj.create_template()
