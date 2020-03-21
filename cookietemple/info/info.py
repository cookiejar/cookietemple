import os
import sys
import click

from ruamel.yaml import YAML
from tabulate import tabulate

from cookietemple.info.levensthein_dist import (most_similar_command, AVAILABLE_HANDLES)
from cookietemple.list.list import load_available_templates
from cookietemple.util.dict_util import is_nested_dictionary


WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/../create/templates'

templates_to_print = []


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

    flatten_nested_dict(template_info)
    click.echo(tabulate(templates_to_print, headers=['Name', 'Handle', 'Description', 'Available Libraries', 'Version']))


    #yaml = YAML()
    #click.echo(click.style(f'Template info for {handle}\n', fg='green'))
    #click.echo()
    #yaml.dump(template_info, sys.stdout)


def flatten_nested_dict(template_info_) -> None:
    """
    This function flattens an arbitrarily deep nested dict and creates a list of list containing all available
    templates for the specified doamin/subdomain and/or language
    :param template_info_: The dict containing the yaml parsed info for all available templates the user wants to
                           gather some information
    """
    if is_nested_dictionary(template_info_):
        for templ in template_info_.values():
            if not is_nested_dictionary(templ):
                templates_to_print.append([templ['name'], templ['handle'], templ['long description'],
                                           templ['available libraries'], templ['version']])
            else:
                flatten_nested_dict(templ)
    else:
        templates_to_print.append([template_info_['name'], template_info_['handle'], template_info_['long description'],
                                   template_info_['available libraries'], template_info_['version']])


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
    most_sim = most_similar_command(handle, AVAILABLE_HANDLES)
    if most_sim:
        if len(most_sim) == 1:
            click.echo(click.style(
                f'cookietemple info: ', fg='white') + click.style(
                f'unknown handle \'{handle}\'. See cookietemple list for all valid handles.\n\nDid you mean\n    \'{most_sim[0]}\'?',
                fg='red'))
        else:
            click.echo(click.style(
                f'cookietemple info: ', fg='white') + click.style(
                f'unknown handle \'{handle}\'. See cookietemple list for all valid handles.\n\nMost similar commands are:',
                fg='red'))
            for command in most_sim:
                click.echo(click.style(f'     {command}', fg='red'))
        sys.exit(0)

    else:
        non_existing_handle()
