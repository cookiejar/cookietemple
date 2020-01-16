import os
import click
from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration,
                                               create_template_with_subdomain_framework, cookiecutter_common_files)
from cookietemple.create.domains.common_language_config.python_config import common_python_options

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"
TEMPLATES_WEB_PATH = f"{WD}/../templates/web"

"""Web Template Versions"""
WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = '0.1.0'


def handle_web():
    """
    Handles the Web domain. Prompts the user for the language, general and domain specific options.

    :return: The version and handle of the chosen template for the .cookietemple file creation.
    """
    language = click.prompt('Please choose between the following languages',
                            type=click.Choice(['Python', 'JavaScript', 'Java'], case_sensitive=False))
    TEMPLATE_STRUCT["language"] = language

    # prompt the user to fetch general template configurations
    prompt_general_template_configuration()

    # switch case statement to prompt the user to fetch template specific configurations
    switcher = {
        'python': common_python_options,
        'javascript': web_javascript_options,
        'java': web_java_options
    }
    switcher.get(language.lower(), lambda: 'Invalid language!')()

    handle_web_project_type_python()

    # switch case statement to fetch the template version
    switcher_version = {
        'python': WEB_WEBSITE_PYTHON_TEMPLATE_VERSION
    }

    return switcher_version.get(language.lower(), lambda: 'Invalid language!'), f"web-{TEMPLATE_STRUCT['webtype']}-{language.lower()}"


def handle_web_project_type_python():
    """
    TODO
    :return:
    """
    TEMPLATE_STRUCT['webtype'] = click.prompt('Please choose between the following web domains',
                                              type=click.Choice(['rest_api', 'website'], case_sensitive=False))

    switcher = {
        'website': handle_website_python,
        'rest_api': handle_rest_api_python
    }
    switcher.get(TEMPLATE_STRUCT['webtype'].lower(), lambda: 'Invalid Web Project Type!')()


def handle_website_python():
    """
    TODO
    :return:
    """
    TEMPLATE_STRUCT['web_framework'] = click.prompt('Please choose between the following frameworks',
                                                    type=click.Choice(['Flask', 'Django'], case_sensitive=False))
    TEMPLATE_STRUCT['url'] = click.prompt('Please enter the project\'s URL (if you have one)',
                                          type=str,
                                          default='dummy.com')

    switcher = {
        'flask': website_flask_options,
        'django': website_django_options
    }
    switcher.get(TEMPLATE_STRUCT["web_framework"].lower(), lambda: 'Invalid Framework!')()


def website_flask_options():
    """
    TODO
    :return:
    """
    TEMPLATE_STRUCT['vm_username'] = click.prompt('Please enter your VM username (if you have one)',
                                                  type=str,
                                                  default='cookietempleuser')

    create_template_with_subdomain_framework(TEMPLATES_WEB_PATH, TEMPLATE_STRUCT['webtype'],
                                             TEMPLATE_STRUCT['language'].lower(),
                                             TEMPLATE_STRUCT['web_framework'].lower())
    cookiecutter_common_files()


def website_django_options():
    print("TODO")


def handle_rest_api_python():
    """Handle REST-API templates"""
    print("TO IMPLEMENT - REST API etc.")


def web_javascript_options():
    print("Implement me")


def web_java_options(some_params):
    print("Implement me")
