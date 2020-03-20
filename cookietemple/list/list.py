import os
import sys

import click

from pathlib import Path
from ruamel.yaml import YAML
from tabulate import tabulate
from flatten_dict import flatten

from cookietemple.util.dict_util import delete_keys_from_dict

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/../create/templates'


def list_available_templates():
    """
    Displays all available templates to stdout in nicely formatted yaml format.
    Omits long descriptions.

    """

    available_templates = load_available_templates(f'{TEMPLATES_PATH}/available_templates.yaml')
    # listing does not need to display the long descriptions of the templates
    # users should use info for long descriptions
    delete_keys_from_dict(available_templates, ['long description'])
    click.echo(click.style('Run cookietemple info for long descriptions of your template of interest.', fg='green'))
    click.echo(click.style('All available templates:\n', fg='green'))

    # What we want to have are lists like
    desired_result = [['Python Commandline Package', 'cli-python', '0.0.1', 'click, argparse', 'General Python package with command line interface']]
    print(tabulate(desired_result, headers=['name', 'handle', 'version', 'available libraries', 'short description']))


def load_available_templates(AVAILABLE_TEMPLATES_PATH):
    """
    Loads 'available_templates.yaml' as a yaml file and returns the content as nested dictionary.

    :return: nested dictionary of all available templates
    """
    path = Path(AVAILABLE_TEMPLATES_PATH)
    yaml = YAML(typ='safe')
    return yaml.load(path)

list_available_templates()
