import logging
import os
import sys

import click

from ruamel.yaml import YAML

from cookietemple.info.levensthein_dist import most_similar_command
from cookietemple.list.list import load_available_templates


console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger('cookietemple info')
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/../create/templates'


def show_info(handle: str):
    """
    Displays detailed information of a domain/language/template

    :param handle: domain/language/template handle (examples: cli or cli-python)
    """
    if not handle:
        handle = click.prompt('Please enter the possibly incomplete template handle as <<domain-(subdomain)-('
                              'language)>>.\nExamples: \'cli-python\' or \'cli\'',
                              type=str)
    click.echo()
    click.echo()
    available_templates = load_available_templates(f'{TEMPLATES_PATH}/available_templates.yaml')

    specifiers = handle.split('-')
    domain = specifiers[0]
    global template_info

    # only domain specified
    if len(specifiers) == 1:
        try:
            template_info = available_templates[domain]
        except KeyError:
            handle_non_existing_command(handle)
    # domain, subdomain, language
    elif len(specifiers) > 2:
        try:
            sub_domain = specifiers[1]
            language = specifiers[2]
            template_info = available_templates[domain][sub_domain][language]
        except KeyError:
            handle_non_existing_command(handle)
    # domain, language OR domain, subdomain
    else:
        try:
            second_specifier = specifiers[1]
            template_info = available_templates[domain][second_specifier]
        except KeyError:
            handle_non_existing_command(handle)

    yaml = YAML()
    click.echo(click.style(f'Template info for {handle}\n', fg='green'))
    click.echo()
    yaml.dump(template_info, sys.stdout)


def non_existing_handle():
    """
    Handling key not found access error for non existing template handles.
    Displays an error message and terminates cookietemple.

    """

    click.echo(click.style('Handle does not exist. Please enter a valid handle. Use ', fg='red')
               + click.style('cookietemple list', fg='blue')
               + click.style(' to display all template handles.', fg='red'))
    sys.exit(0)


def handle_non_existing_command(handle: str):
    most_sim = most_similar_command(handle)
    if most_sim != "":
        click.echo(click.style(
            f'cookietemple info: ', fg='white') + click.style(
            f'unknown handle \'{handle}\'. See cookietemple list for all valid handles.\n\nDid you mean\n    \'{most_sim}\'?',
            fg='red'))
        sys.exit(0)
    else:
        non_existing_handle()
