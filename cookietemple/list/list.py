import os

import click

from pathlib import Path
from ruamel.yaml import YAML
from rich.style import Style
from rich.console import Console
from rich.table import Table
from rich.box import HEAVY_HEAD

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

    # What we want to have are lists like
    # [['name', 'handle', 'short description', 'available libraries', 'version'], ['name', 'handle', 'short description', 'available libraries', 'version']]
    templates_to_tabulate = []
    for language in available_templates.values():
        assert is_nested_dictionary(language)
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

    table = Table(title="[bold]All available COOKIETEMPLE templates", title_style="blue", header_style=Style(color="blue", bold=True), box=HEAVY_HEAD)

    table.add_column("Name", justify="center", style="green", no_wrap=True)
    table.add_column("Handle", justify="center")
    table.add_column("Short Description", justify="center")
    table.add_column("Available Libraries", justify="center")
    table.add_column("Version", justify="center")

    for template in templates_to_tabulate:
        table.add_row(f'[bold]{template[0]}', template[1], template[2], template[3], template[4])

    console = Console()
    console.print(table)


def load_available_templates(AVAILABLE_TEMPLATES_PATH) -> dict:
    """
    Loads 'available_templates.yaml' as a yaml file and returns the content as nested dictionary.

    :return: nested dictionary of all available templates
    """
    path = Path(AVAILABLE_TEMPLATES_PATH)
    yaml = YAML(typ='safe')
    return yaml.load(path)
