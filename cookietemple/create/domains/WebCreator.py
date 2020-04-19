import os
import click
from pathlib import Path
from dataclasses import dataclass

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.domains.common_language_config.python_config import common_python_options
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.util.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructWeb(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for WEB projects
    This section contains some attributes specific for WEB-domain projects
    """
    # TODO: Currently only python but this will be refactored as we have more templates
    webtype: str = ""  # the type of web project like website or REST-API

    """
    This section contains some attributes specific for website projects
    """
    web_framework: str = ""  # the framework, the user wants to use (if any)
    is_basic_website: str = ""  # indicates whether the user wants a basic website setup or a more advanced with database support etc.
    url: str = ""  # the url for the website (if any)

    """
    This section contains some attributes specific for website projects
    """
    vm_username: str = ""  # the username (if any) for a VM (only necessary for Deployment in a Linux VM)


class WebCreator(TemplateCreator):

    def __init__(self):
        self.web_struct = TemplateStructWeb(domain='web')
        super().__init__(self.web_struct)
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_WEB_PATH = f'{self.WD}/../templates/web'

        '""Web Template Versions""'
        self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = super().load_version('web-website-python')

    def create_template(self) -> None:
        """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.
        """
        self.web_struct.language = click.prompt('Please choose between the following languages [python, javascript, java]',
                                                type=click.Choice(['python', 'javascript', 'java']))

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': common_python_options,
            'javascript': web_javascript_options,
            'java': web_java_options
        }
        switcher.get(self.web_struct.language.lower(), lambda: 'Invalid language!')(self.creator_ctx)

        if self.web_struct.language == 'python':
            self.handle_web_project_type_python()

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION
        }

        self.web_struct.template_version, self.web_struct.template_handle = switcher_version.get(
            self.web_struct.language.lower(), lambda: 'Invalid language!'), f"web-{self.web_struct.webtype}-{self.web_struct.language.lower()}"

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations()

    def handle_web_project_type_python(self) -> None:
        """
        Determine the type of web application and handle it further.
        """
        self.web_struct.webtype = click.prompt('Please choose between the following web domains [rest_api, website]',
                                               type=click.Choice(['rest_api', 'website']))

        switcher = {
            'website': self.handle_website_python,
            'rest_api': self.handle_rest_api_python
        }
        switcher.get(self.web_struct.webtype.lower(), lambda: 'Invalid Web Project Type!')()

    def handle_website_python(self) -> None:
        """
        Handle the website template creation. The user can choose between a basic website setup and a more advanced
        with database support, mail, translation, cli commands for translation, login and register function.
        """
        self.web_struct.web_framework = click.prompt('Please choose between the following frameworks [flask, django]',
                                                     type=click.Choice(['flask', 'django']))
        setup = click.prompt(
            'Choose between basic or advanced (database, translations, deployment scripts) [basic, advanced]:',
            type=click.Choice(['basic', 'advanced']),
            default='basic')
        self.web_struct.is_basic_website = 'y'

        if setup == 'advanced':
            self.web_struct.is_basic_website = 'n'

        self.web_struct.url = click.prompt('Please enter the project\'s URL (if you have one)',
                                           type=str,
                                           default='dummy.com')

        switcher = {
            'flask': self.website_flask_options,
            'django': self.website_django_options
        }
        switcher.get(self.web_struct.web_framework.lower(), lambda: 'Invalid Framework!')()

    def website_flask_options(self) -> None:
        """
        Create a flask website template.
        """
        self.web_struct.vm_username = click.prompt('Please enter your VM username (if you have one)',
                                                   type=str,
                                                   default='cookietempleuser')

        super().create_template_with_subdomain_framework(self.TEMPLATES_WEB_PATH, self.web_struct.webtype, self.web_struct.web_framework.lower())

        self.remove_basic_or_advanced_files(self.web_struct.is_basic_website)

    def remove_basic_or_advanced_files(self, is_basic: str) -> None:
        """
        Remove the dir/files that do not belong in a basic/advanced template.

        :param is_basic: Shows whether the user sets up a basic or advanced website setup
        """
        cwd = os.getcwd()
        os.chdir(f"{cwd}/{self.web_struct.project_slug}/{self.web_struct.project_slug}")

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

    def website_django_options(self):
        print('TODO')

    def handle_rest_api_python(self):
        """Handle REST-API templates"""
        print('TO IMPLEMENT - REST API etc.')


def web_javascript_options():
    print('Implement me')


def web_java_options(some_params):
    print('Implement me')
