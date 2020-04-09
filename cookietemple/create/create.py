import os
import click

from cookietemple.create.create_config import (TEMPLATE_STRUCT)
from cookietemple.create.domains.CliCreator import CliCreator


WD = os.path.dirname(__file__)
CWD = os.getcwd()


def choose_domain(domain: str):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    """

    if not domain:
        TEMPLATE_STRUCT['domain'] = click.prompt('Choose between the following domains [cli, gui, web]',
                                                 type=click.Choice(['cli', 'gui', 'web']))
    else:
        TEMPLATE_STRUCT['domain'] = domain

    switcher = {
        'cli': CliCreator,
        'web': 'web',
        'gui': 'gui'
    }

    creator_obj = switcher.get(TEMPLATE_STRUCT['domain'].lower(), lambda: 'Invalid domain!')()
    creator_obj.create_template()

