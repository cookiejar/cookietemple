import os
from pathlib import Path

import click

from cookietemple.create.create_config import TEMPLATE_STRUCT
from cookietemple.create.create_templates import create_template_with_subdomain

WD = os.path.dirname(__file__)
WD_Path = Path(WD)
TEMPLATES_PATH = f'{WD}/../templates'
TEMPLATES_PUB_PATH = f'{WD_Path.parent}/templates/pub'

'"" TEMPLATE VERSIONS ""'
PUB_LATEX_TEMPLATE_VERSION = '0.1.0'


def handle_pub():
    """

    :return:
    """

    # language = click.prompt('Choose between the following languages [latex]',
    #                        type=click.Choice(['latex']))
    language = 'latex'
    TEMPLATE_STRUCT['language'] = language

    # prompt the user to fetch general template configurations
    # prompt_general_template_configuration()

    TEMPLATE_STRUCT['pubtype'] = click.prompt('Please choose between the following publication types [thesis, paper]',
                                              type=click.Choice(['thesis', 'paper']))

    # switch case statement to prompt the user to fetch template specific configurations
    switcher = {
        'latex': common_latex_options,
    }
    switcher.get(language.lower(), lambda: 'Invalid language!')()

    handle_pub_type()

    create_template_with_subdomain(TEMPLATES_PUB_PATH, TEMPLATE_STRUCT['pubtype'],
                                   TEMPLATE_STRUCT['language'].lower())

    # create the common files and copy them into the templates directory
    # create_common_files()

    # switch case statement to fetch the template version
    switcher_version = {
        'latex': PUB_LATEX_TEMPLATE_VERSION,
    }

    return switcher_version.get(language.lower(), lambda: 'Invalid language!'), f"pub-{TEMPLATE_STRUCT['pubtype']}-{language.lower()}"


def handle_pub_type() -> None:
    """
    Determine the type of publication and handle it further.
    """

    switcher = {
        'website': handle_thesis_latex,
        'rest_api': handle_paper_latex
    }
    switcher.get(TEMPLATE_STRUCT['pubtype'].lower(), lambda: 'Invalid Pub Project Type!')()


def handle_thesis_latex() -> None:
    pass


def handle_paper_latex() -> None:
    pass


def common_latex_options() -> None:
    """

    """
    TEMPLATE_STRUCT['project_slug'] = click.prompt('Project Slug:',
                                                   type=str,
                                                   default='Cookietemple_thesis_template')
    TEMPLATE_STRUCT['title'] = click.prompt('Thesis Title:',
                                            type=str,
                                            default='On how Springfield exploded')
    TEMPLATE_STRUCT['author'] = click.prompt('Author:',
                                             type=str,
                                             default='Homer Simpson')
    TEMPLATE_STRUCT['university'] = click.prompt('University:',
                                                 type=str,
                                                 default='Homer J. Simpson University')
    TEMPLATE_STRUCT['deparment'] = click.prompt('Department:',
                                                type=str,
                                                default='Department of nuclear physics')
    TEMPLATE_STRUCT['degree'] = click.prompt('Degree:',
                                             type=str,
                                             default='PhD')
