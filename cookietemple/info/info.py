import logging
import os
import sys

import click

from ruamel.yaml import YAML

from cookietemple.list.list import load_available_templates

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("cookietemple info")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../create/templates"


@click.command()
@click.option('--handle',
              type=str,
              help='Possibly incomplete handle of the template. Use \'cookietemple list\' to show the handles of all templates or enter an incomplete handle to display all sub options.',
              prompt=click.style('Please enter the possibly incomplete template handle.\n'
                     'Examples: ')
                     + click.style('cli-python', fg='blue')
                     + click.style(' or ')
                     + click.style('cli', fg='blue'))
def info(handle):
    available_templates = load_available_templates(f"{TEMPLATES_PATH}/available_templates.yaml")
    click.echo()
    click.echo(click.style(f"Template info for {handle}\n", fg='green'))

    specifiers = handle.split('-')
    domain = specifiers[0]
    global template_info

    # only domain specified
    if len(specifiers) == 1:
        try:
            template_info = available_templates[domain]
        except KeyError:
            non_existing_handle()
    # domain, subdomain, language
    elif len(specifiers) > 2:
        try:
            sub_domain = specifiers[1]
            language = specifiers[2]
            template_info = available_templates[domain][sub_domain][language]
        except KeyError:
            non_existing_handle()
    # domain, language OR domain, subdomain
    else:
        try:
            second_specifier = specifiers[1]
            template_info = available_templates[domain][second_specifier]
        except KeyError:
            non_existing_handle()

    yaml = YAML()
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
