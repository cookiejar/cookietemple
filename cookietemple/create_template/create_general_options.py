import sys

import click

from cookietemple.create_template.create_config import TEMPLATE_STRUCT


@click.command()
@click.option('--full_name',
              type=str,
              help='Your full name.',
              prompt='Please enter your full name',
              default='Homer Simpson')
@click.option('--email',
              type=str,
              help='Your personal or work email.',
              prompt='Please enter your personal or work email',
              default='homer.simpson@example.com')
@click.option('--github_username',
              type=str,
              help='We require your github username for automatic deployment and uploading your newly created project to your repository',
              prompt='Please enter your github account name',
              default='homersimpson')
@click.option('--project_name',
              type=str,
              help='The name of your project.',
              prompt='Please enter your project name of choice',
              default='Python CLI')
@click.option('--project_slug',
              type=str,
              help='The name of your project in an URL friendly manner. Refrain from using spaces or uncommon letters.',
              prompt='Please enter an URL friendly project slug',
              default='Python-CLI')
@click.option('--project_short_description',
              type=str,
              help='A short description of your project. 2-3 sentences may suffice. There is room for more detailed descriptions in your documentation.',
              prompt='Please enter a short description of your project',
              default='Python CLI contains all the boilerplate you need to create a Python package with commandline support.')
@click.option('--create_author_file/--no_author_file',
              help='Whether or not an author file containing all contributing authors should be created.',
              prompt='Please determine whether or not an author file should be created.',
              default=True)
@click.option('--version',
              type=str,
              help='The initial version of your project. It is recommended to follow the semantic version convention (https://semver.org/)',
              prompt='Please enter the initial version number',
              default='0.1.0')
@click.option('--license',
              type=click.Choice(['MIT', 'BSD', 'ISC', 'Apache2.0', 'GNUv3', 'Not open source'], case_sensitive=False),
              help='To get more information on the available licenses and to choose the best fitting license for your project we recommend choosealicense.com/',
              prompt='Please choose a license.',
              default='MIT')
def determine_general_options(full_name, email, github_username, project_name, project_slug, project_short_description, create_author_file, version, license):
    TEMPLATE_STRUCT['full_name'] = full_name
    TEMPLATE_STRUCT['email'] = email
    TEMPLATE_STRUCT['github_username'] = github_username
    TEMPLATE_STRUCT['project_name'] = project_name
    TEMPLATE_STRUCT['project_slug'] = project_slug
    TEMPLATE_STRUCT['project_short_description'] = project_short_description
    TEMPLATE_STRUCT['version'] = version
    TEMPLATE_STRUCT['license'] = license

    if create_author_file:
        TEMPLATE_STRUCT['create_author_file'] = 'y'
    else:
        TEMPLATE_STRUCT['create_author_file'] = 'n'

    sys.exit()
