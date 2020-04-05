import os
import click
import re

# The main dictionary, which will be completed by first the general options prompts and then the chosen template
# specific prompts. It is then passed onto cookiecutter as extra_content to facilitate the template creation.
# Finally, it is also used for the creation of the .cookietemple file.

TEMPLATE_STRUCT = {}

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/templates'
COMMON_FILES_PATH = f'{WD}/templates/common_files'


def prompt_general_template_configuration():
    """
    Prompts the user for general options that are required by all templates.
    Options are saved in the TEMPLATE_STRUCT dict.
    """

    TEMPLATE_STRUCT['full_name'] = click.prompt('Please enter your full name',
                                                type=str,
                                                default='Homer Simpson')
    TEMPLATE_STRUCT['email'] = click.prompt('Please enter your personal or work email',
                                            type=str,
                                            default='homer.simpson@example.com')
    TEMPLATE_STRUCT['project_name'] = click.prompt('Please enter your project name',
                                                   type=str,
                                                   default='Exploding Springfield')
    TEMPLATE_STRUCT['project_slug'] = TEMPLATE_STRUCT['project_name'].replace(' ', '_')
    TEMPLATE_STRUCT['project_short_description'] = click.prompt('Please enter a short description of your project.',
                                                                type=str,
                                                                default=f'{TEMPLATE_STRUCT["project_name"]}. A best practice .')

    poss_vers = click.prompt('Please enter the initial version of your project.',
                             type=str,
                             default='0.1.0')

    while not re.match(r'[0-9]+.[0-9]+.[0-9]+', poss_vers):
        click.echo(click.style('The version number entered does not match cookietemples pattern.\n'
                               'Please enter the version in the format [number].[number].[number]!', fg='red'))
        poss_vers = click.prompt('Please enter the initial version of your project.',
                                 type=str,
                                 default='0.1.0')

    TEMPLATE_STRUCT['version'] = poss_vers

    TEMPLATE_STRUCT['license'] = click.prompt(
        'Please choose a license [MIT, BSD, ISC, Apache2.0, GNUv3, Not open source]',
        type=click.Choice(['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Not open source']),
        default='MIT')
