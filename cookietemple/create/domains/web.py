import os
import click
from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration)
from cookietemple.create.domains.common_language_config.python_config import common_python_options

from cookiecutter.main import cookiecutter


WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"
TEMPLATES_WEB_PATH = f"{WD}/../templates/web"

"""Web Template Versions"""
WEB_PYTHON_TEMPLATE_VERSION = '0.1.0'


@click.command()
@click.option('--language',
              type=click.Choice(['Python', 'JavaScript', 'Java'], case_sensitive=False),
              prompt="Choose between the following languages for your web project:")
def handle_web(language):
    """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.

        :return: The version and handle of the chosen template for the .cookietemple file creation.
    """

    TEMPLATE_STRUCT["language"] = language

    # prompt the user to fetch general template configurations
    prompt_general_template_configuration(standalone_mode=False)

    # switch case statement to prompt the user to fetch template specific configurations
    switcher = {
        'python': common_python_options,
        'javascript': web_javascript_options,
        'java': web_java_options
    }
    switcher.get(language.lower(), lambda: 'Invalid language!')(standalone_mode=False)

    handle_web_project_type_python(standalone_mode=False)

    # switch case statement to fetch the template version
    switcher_version = {
        'python': WEB_PYTHON_TEMPLATE_VERSION
    }

    return switcher_version.get(language.lower(), lambda: 'Invalid language!'), f"cli-{language.lower()}"




@click.command()
@click.option('--webtype',
              type=click.Choice(['WebApplication', 'Website'], case_sensitive=False),
              prompt="Choose between the following types for your web project:")
def handle_web_project_type_python(webtype):
    """Determine which type of web project the user wants to generate a template for"""

    TEMPLATE_STRUCT["webtype"] = webtype

    switcher = {
        'website': handle_website_python,
        'webapplication': handle_web_app_python
    }
    switcher.get(webtype.lower(), lambda: 'Invalid Web Project Type!')(standalone_mode=False)


@click.command()
@click.option('--framework',
              type=click.Choice(['Flask', 'Django'], case_sensitive=False),
              prompt="Choose between the following frameworks for your website project:")
@click.option('--url',
              help='Specify your URL (if you already have one for your project)',
              prompt='Please enter the project´s URL (if you have one).',
              default='dummy.com')
def handle_website_python(framework,url):
    """Handle website templates with python"""
    TEMPLATE_STRUCT['web_framework'] = framework
    TEMPLATE_STRUCT['url'] = url

    switcher = {
        'flask': website_flask_options,
        'django': website_django_options
    }
    switcher.get(framework.lower(), lambda: 'Invalid Framework!')(standalone_mode=False)


def handle_web_app_python():
    """Handle Web App Templates"""
    print("TO IMPLEMENT - REST API etc.")




@click.command()
@click.option('--user_vm_name',
              help='Your Server VM Name for deployment of your application',
              prompt='Please enter your VM Name (if you have one).',
              default='dummyVM')
def website_flask_options(user_vm_name):

    TEMPLATE_STRUCT['uservmname'] = user_vm_name
    create_cookietemple_website_template()


def create_cookietemple_website_template():
    # create the chosen and configured template
    cookiecutter(f"{TEMPLATES_WEB_PATH}/website_{TEMPLATE_STRUCT['language'].lower()}/{TEMPLATE_STRUCT['web_framework'].lower()}",
                 no_input=True,
                 overwrite_if_exists=True,
                 extra_context=TEMPLATE_STRUCT)






def website_django_options():
    print("TODO")

def web_javascript_options():
    print("Implement me")

def web_java_options(some_params):
    print("Implement me")
