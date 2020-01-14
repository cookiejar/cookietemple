import os
import tempfile
import shutil
from distutils.dir_util import copy_tree
import click
import yaml
from cookiecutter.main import cookiecutter

# The main dictionary, which will be completed by first the general options prompts and then the chosen template specific prompts.
# It is then passed onto cookiecutter as extra_content to facilitate the template creation.
# Finally, it is also used for the creation of the .cookietemple file.
TEMPLATE_STRUCT = {}

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/templates"
COMMON_FILES_PATH = f"{WD}/templates/common_files"


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
def prompt_general_template_configuration(full_name, email, github_username, project_name, project_slug,
                                          project_short_description,
                                          version, license):
    """
    Prompts the user for general options that are required by all templates.
    Options are saved in the TEMPLACE_STRUCT dict.
    """

    TEMPLATE_STRUCT['full_name'] = full_name
    TEMPLATE_STRUCT['email'] = email
    TEMPLATE_STRUCT['github_username'] = github_username
    TEMPLATE_STRUCT['project_name'] = project_name
    TEMPLATE_STRUCT['project_slug'] = project_slug
    TEMPLATE_STRUCT['project_short_description'] = project_short_description
    TEMPLATE_STRUCT['version'] = version
    TEMPLATE_STRUCT['license'] = license


def create_dot_cookietemple(TEMPLATE_STRUCT: dict, template_version: str, template_handle: str):
    """
    Overrides the version with the version of the template.
    Dumps the configuration for the template generation into a .cookietemple yaml file.

    :param TEMPLATE_STRUCT: Global variable containing all cookietemple creation configuration variables
    :param template_version: Version of the specific template
    """
    TEMPLATE_STRUCT['template_version'] = template_version
    TEMPLATE_STRUCT['template_handle'] = template_handle
    with open(f'{TEMPLATE_STRUCT["project_slug"]}/.cookietemple', 'w') as f:
        yaml.dump(TEMPLATE_STRUCT, f)


def create_cookietemple_website_template(web_path, web_type, language, framework):
    # create the chosen and configured website template
    cookiecutter(f"{web_path}/{web_type}_{language}/{framework}",
                 no_input=True,
                 overwrite_if_exists=True,
                 extra_context=TEMPLATE_STRUCT)


def cookiecutter_common_files():
    """
    This function creates a temporary directory for common files of all templates and applies cookiecutter on them.

    It´ll be outputted to the created template directory.
    """
    dirpath = tempfile.mkdtemp()
    copy_tree(f"{COMMON_FILES_PATH}", dirpath)
    cookiecutter(dirpath,
                 extra_context={"commonName": "common_files_util"},
                 no_input=True,
                 overwrite_if_exists=True,
                 output_dir=f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
    shutil.rmtree(dirpath)
