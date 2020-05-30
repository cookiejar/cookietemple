import click

from cookietemple.create.domains.cli_creator import CliCreator
from cookietemple.create.domains.web_creator import WebCreator
from cookietemple.create.domains.gui_creator import GuiCreator
from cookietemple.create.domains.pub_creator import PubCreator


def choose_domain(domain: str):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    """

    if not domain:
        domain = click.prompt('Choose between the following domains [cli, gui, web, pub]',
                              type=click.Choice(['cli', 'gui', 'web', 'pub']))

    switcher = {
        'cli': CliCreator,
        'web': WebCreator,
        'gui': GuiCreator,
        'pub': PubCreator
    }

    creator_obj = switcher.get(domain.lower(), lambda: 'Invalid domain!')()
    creator_obj.create_template()
