import os
import click
from pathlib import Path
from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration)
from cookietemple.create.create_templates import create_template_with_subdomain_framework, create_common_files, delete_dir_tree
from cookietemple.create.domains.common_language_config.python_config import common_python_options

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f'{WD}/../templates'
TEMPLATES_WEB_PATH = f'{WD}/../templates/web'

'""Web Template Versions""'
WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = '0.1.0'


def handle_web():
    """
    Handles the Web domain. Prompts the user for the language, general and domain specific options.

    :return: The version and handle of the chosen template for the .cookietemple file creation.
    """
    language = click.prompt('Please choose between the following languages [python, javascript, java]',
                            type=click.Choice(['python', 'javascript', 'java']))
    TEMPLATE_STRUCT['language'] = language

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
    Determine the type of web application and handle it further.
    """
    TEMPLATE_STRUCT['webtype'] = click.prompt('Please choose between the following web domains [rest_api, website]',
                                              type=click.Choice(['rest_api', 'website']))

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
    TEMPLATE_STRUCT['web_framework'] = click.prompt('Please choose between the following frameworks [flask, django]',
                                                    type=click.Choice(['flask', 'django']))
    setup = click.prompt(
        'Choose between basic or advanced (database, translations, deployment scripts) [basic, advanced]:',
        type=click.Choice(['basic', 'advanced']),
        default='basic')
    TEMPLATE_STRUCT['is_basic_website'] = 'y'

    if setup == 'advanced':
        TEMPLATE_STRUCT['is_basic_website'] = 'n'

    TEMPLATE_STRUCT['url'] = click.prompt('Please enter the project\'s URL (if you have one)',
                                          type=str,
                                          default='dummy.com')

    switcher = {
        'flask': website_flask_options,
        'django': website_django_options
    }
    switcher.get(TEMPLATE_STRUCT['web_framework'].lower(), lambda: 'Invalid Framework!')()


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
    create_common_files()

    remove_basic_or_advanced_files(TEMPLATE_STRUCT['is_basic_website'])


def remove_basic_or_advanced_files(is_basic: str) -> None:
    """
    Remove the dir/files that do not belong in a basic/advanced template.

    :param is_basic: Shows whether the user sets up a basic or advanced website setup
    """
    cwd = os.getcwd()
    os.chdir(f"{cwd}/{TEMPLATE_STRUCT['project_slug']}/{TEMPLATE_STRUCT['project_slug']}")

    if is_basic == 'y':
        delete_dir_tree(Path('translations'))
        delete_dir_tree(Path('auth'))
        delete_dir_tree(Path('models'))
        delete_dir_tree(Path('services'))
        delete_dir_tree(Path('templates/auth'))
        os.remove('templates/index.html')
        os.remove('templates/base.html')
        os.remove('static/mail_stub.conf')
        os.remove('../babel.cfg')

    elif is_basic == 'n':
        delete_dir_tree(Path('templates/basic'))
        delete_dir_tree(Path('basic'))

    os.chdir(cwd)


def website_django_options():
    print('TODO')


def handle_rest_api_python():
    '""Handle REST-API templates""'
    print('TO IMPLEMENT - REST API etc.')


def web_javascript_options():
    print('Implement me')


def web_java_options(some_params):
    print('Implement me')
