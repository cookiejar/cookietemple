import os

import click

from pathlib import Path
from ruamel.yaml import YAML
from tabulate import tabulate

from cookietemple.util.dict_util import is_nested_dictionary

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/../create/templates'


def list_available_templates() -> None:
    """
    Displays all available templates to stdout in nicely formatted yaml format.
    Omits long descriptions.

    """

    available_templates = load_available_templates(f'{TEMPLATES_PATH}/available_templates.yml')
    click.echo(click.style('Run ', fg='blue')
               + click.style('cookietemple info ', fg='green')
               + click.style('for long descriptions of your template of interest.', fg='blue'))
    click.echo(click.style('All available templates:\n', fg='blue'))

    # What we want to have are lists like
    # [['name', 'handle', 'short description', 'available libraries', 'version'], ['name', 'handle', 'short description', 'available libraries', 'version']]
    templates_to_tabulate = []
    for language in available_templates.values():
        for val in language.values():
            # has a subdomain -> traverse dictionary a level deeper
            if is_nested_dictionary(val):
                for val_2 in val.values():
                    templates_to_tabulate.append([
                        val_2['name'], val_2['handle'], val_2['short description'], val_2['available libraries'], val_2['version']
                    ])
            else:
                templates_to_tabulate.append([
                    val['name'], val['handle'], val['short description'], val['available libraries'], val['version']
                ])

    # Print nicely to console
    click.echo(tabulate(templates_to_tabulate, headers=['Name', 'Handle', 'Short Description', 'Available Libraries', 'Version']))


def load_available_templates(AVAILABLE_TEMPLATES_PATH) -> dict:
    """
    Loads 'available_templates.yaml' as a yaml file and returns the content as nested dictionary.

    :return: nested dictionary of all available templates
    """
    path = Path(AVAILABLE_TEMPLATES_PATH)
    yaml = YAML(typ='safe')
    return yaml.load(path)
