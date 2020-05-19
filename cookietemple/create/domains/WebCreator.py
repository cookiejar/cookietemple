import os
import click
from pathlib import Path
from dataclasses import dataclass
from distutils.dir_util import copy_tree
from shutil import copy

from cookietemple.create.TemplateCreator import TemplateCreator
from cookietemple.create.domains.common_language_config.python_config import common_python_options
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructWeb(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for WEB projects
    This section contains some attributes specific for WEB-domain projects
    """
    # TODO: Currently only python but this will be refactored as we have more templates
    webtype: str = ''  # the type of web project like website or REST-API

    """
    This section contains some attributes specific for website projects
    """
    web_framework: str = ''  # the framework, the user wants to use (if any)
    is_basic_website: str = ''  # indicates whether the user wants a basic website setup or a more advanced with database support etc.
    use_frontend: str = ''  # indicates whether the user wants a shipped with frontend template or not
    frontend: str = ''  # the name of the frontend template (if any; the user has several options)
    url: str = ''  # the url for the website (if any)

    """
    This section contains some attributes specific for website projects
    """
    vmusername: str = ''  # the username (if any) for a VM (only necessary for Deployment in a Linux VM)


class WebCreator(TemplateCreator):

    def __init__(self):
        self.web_struct = TemplateStructWeb(domain='web')
        super().__init__(self.web_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_WEB_PATH = f'{self.WD_Path.parent}/templates/web'

        '""Web Template Versions""'
        self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = super().load_version('web-website-python')

    def create_template(self) -> None:
        """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.
        """
        self.web_struct.language = click.prompt('Please choose between the following languages [python, javascript, java]',
                                                type=click.Choice(['python', 'javascript', 'java'])).lower()

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
            self.web_struct.language.lower(), lambda: 'Invalid language!'), f'web-{self.web_struct.webtype}-{self.web_struct.language.lower()}'

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

        self.web_struct.use_frontend = click.confirm('Do you want to initialize your project with a advanced frontend template?')

        # prompt the user for its frontend template, if he wants so
        if self.web_struct.use_frontend:
            click.echo(click.style('The following templates are available:\n', fg='blue'))

            # strings that start with https: are recognized by most terminal (emulators) as links
            click.echo(click.style('https://html5up.net/solid-state', fg='blue'))

            self.web_struct.frontend = click.prompt('Enter your preferred template or None, if you didn´t like them [Solid State, None]',
                                                    type=click.Choice(['SolidState', 'None'])).lower()

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
        self.web_struct.vmusername = click.prompt('Please enter your VM username (if you have one)',
                                                  type=str,
                                                  default='cookietempleuser')

        super().create_template_with_subdomain_framework(self.TEMPLATES_WEB_PATH, self.web_struct.webtype, self.web_struct.web_framework.lower())

        self.basic_or_advanced_files_with_frontend(self.web_struct.is_basic_website, self.web_struct.frontend.lower())

    def basic_or_advanced_files_with_frontend(self, is_basic: str, template_name: str) -> None:
        """
        Remove the dir/files that do not belong in a basic/advanced template and add a full featured frontend template
        if the user wants so.

        :param is_basic: Shows whether the user sets up a basic or advanced website setup
        :param template_name: the name of the frontend template (if any)
        """
        cwd = os.getcwd()
        os.chdir(f'{cwd}/{self.web_struct.project_slug}/{self.web_struct.project_slug}')

        # remove all stuff, that is not necessary for the basic setup
        if is_basic == 'y':
            delete_dir_tree(Path('translations'))
            delete_dir_tree(Path('auth'))
            delete_dir_tree(Path('main'))
            delete_dir_tree(Path('models'))
            delete_dir_tree(Path('services'))
            delete_dir_tree(Path('templates/auth'))
            os.remove('templates/index.html')
            os.remove('templates/base.html')
            os.remove('static/mail_stub.conf')
            os.remove('../babel.cfg')

            # the user wants only minimal frontend, so remove the index html file for this
            if not template_name or template_name == 'none':
                os.remove('templates/basic_index_f.html')

        # remove basic stuff in advanced setup
        elif is_basic == 'n':
            delete_dir_tree(Path('basic'))

        # the user wants to init its project with a full frontend
        if template_name and template_name != 'none':
            copy_tree(f'../frontend_templates/{template_name}/assets', 'static/assets')
            copy(f'../frontend_templates/{template_name}/index.html', 'templates')

            # remove unnecessary files for basic frontend setup
            if is_basic == 'y':
                os.remove('templates/basic_index.html')
                os.remove('templates/index.html')
            # remove unnecessary files for advanced frontend setup
            else:
                os.remove('templates/basic_index_f.html')
                os.remove('templates/basic_index.html')

        else:
            # remove basic html files if advanced setup
            if is_basic == 'n':
                os.remove('templates/basic_index.html')
                os.remove('templates/basic_index_f.html')

        # remove all frontend stuff
        delete_dir_tree(Path('../frontend_templates'))

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
