import os
from collections import OrderedDict

import click
from pathlib import Path
from dataclasses import dataclass
from distutils.dir_util import copy_tree
from shutil import copy

from cookietemple.create.template_creator import TemplateCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.create.github_support import prompt_github_repo
from cookietemple.common.version import load_ct_template_version


@dataclass
class TemplateStructWeb(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for WEB projects
    This section contains some attributes specific for WEB-domain projects
    """
    # TODO: Currently only python but this will be refactored as we have more templates
    webtype: str = ''  # the type of web project like website or REST-API

    """
    General Python attributes
    """
    command_line_interface: str = ''  # which command line library to use (click, argparse)
    testing_library: str = ''  # which testing library to use (pytest, unittest)

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
        self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = load_ct_template_version('web-website-python', self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, dot_cookietemple: dict or None) -> None:
        """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.
        """
        self.web_struct.language = cookietemple_questionary_or_dot_cookietemple('select', 'Choose between the following languages', ['python'])

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_cookietemple)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher = {
            'python': self.web_python_options,
        }
        switcher.get(self.web_struct.language)(dot_cookietemple)

        if self.web_struct.language == 'python':
            self.handle_web_project_type_python(dot_cookietemple)

        # switch case statement to fetch the template version
        switcher_version = {
            'python': self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION
        }

        self.web_struct.template_version, self.web_struct.template_handle = switcher_version.get(
            self.web_struct.language), f'web-{self.web_struct.webtype}-{self.web_struct.language.lower()}'

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(domain='web',
                                          subdomain=self.web_struct.webtype,
                                          language=self.web_struct.language,
                                          dot_cookietemple=dot_cookietemple)

    def handle_web_project_type_python(self, dot_cookietemple: dict or None) -> None:
        """
        Determine the type of web application and handle it further.
        """
        self.web_struct.webtype = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                               question='Choose between the following web domains',
                                                                               choices=['website'],
                                                                               default='website',
                                                                               dot_cookietemple=dot_cookietemple,
                                                                               to_get_property='webtype')

        switcher = {
            'website': self.handle_website_python,
        }
        switcher.get(self.web_struct.webtype.lower())(dot_cookietemple)

    def handle_website_python(self, dot_cookietemple: dict or None) -> None:
        """
        Handle the website template creation. The user can choose between a basic website setup and a more advanced
        with database support, mail, translation, cli commands for translation, login and register function.
        """
        self.web_struct.web_framework = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                     question='Choose between the following frameworks',
                                                                                     choices=['flask'],
                                                                                     default='flask',
                                                                                     dot_cookietemple=dot_cookietemple,
                                                                                     to_get_property='web_framework')
        setup = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                             question='Choose between the basic and advanced'
                                                                      ' (database, translations, deployment scripts) template',
                                                             choices=['basic', 'advanced'],
                                                             default='basic',
                                                             dot_cookietemple=dot_cookietemple,
                                                             to_get_property='setup')
        # COOKIETEMPLE TODO This MUST be refactored into a webstruct.setup_type or something of that sort -> don't use y/n as properties
        self.web_struct.is_basic_website = 'y'

        if setup == 'advanced':
            self.web_struct.is_basic_website = 'n'

        self.web_struct.use_frontend = cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                                                    question='Do you want to initialize your project'
                                                                                             ' with a advanced frontend template?',
                                                                                    default='Yes',
                                                                                    dot_cookietemple=dot_cookietemple,
                                                                                    to_get_property='use_frontend')

        # prompt the user for its frontend template, if he wants so
        if self.web_struct.use_frontend:
            click.echo(click.style('The following templates are available:\n', fg='blue'))

            # strings that start with https: are recognized by most terminal (emulators) as links
            click.echo(click.style('https://html5up.net/solid-state', fg='blue'))

            self.web_struct.frontend = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                    question='Choose between the following predefined frontend templates',
                                                                                    choices=['SolidState', 'None'],
                                                                                    dot_cookietemple=dot_cookietemple,
                                                                                    to_get_property='frontend').lower()

        self.web_struct.url = cookietemple_questionary_or_dot_cookietemple(function='text',
                                                                           question='Project URL (if already existing)',
                                                                           default='dummy.com',
                                                                           dot_cookietemple=dot_cookietemple,
                                                                           to_get_property='url')

        switcher = {
            'flask': self.website_flask_options,
            'django': self.website_django_options
        }
        switcher.get(self.web_struct.web_framework.lower())(dot_cookietemple)

    def website_flask_options(self, dot_cookietemple: OrderedDict or None) -> None:
        """
        Create a flask website template.
        """
        # prompt username for virtual machine (needed for example when deploying from a Linux VM)
        self.web_struct.vmusername = cookietemple_questionary_or_dot_cookietemple(function='text',
                                                                                  question='Virtual machine username (if already existing)',
                                                                                  default='cookietempleuser',
                                                                                  dot_cookietemple=dot_cookietemple,
                                                                                  to_get_property='vmusername')
        # prompt github repo creation
        self.web_prompt_github(dot_cookietemple)
        # if repo owner is a github orga, update username
        if self.web_struct.is_github_orga:
            self.web_struct.github_username = self.web_struct.github_orga

        # create the flask web project
        super().create_template_with_subdomain_framework(self.TEMPLATES_WEB_PATH, self.web_struct.webtype, self.web_struct.web_framework.lower())
        # clean project for advanced or basic setup
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

    def web_python_options(self, dot_cookietemple: OrderedDict or None):
        """ Prompts for web-python specific options and saves them into the CookietempleTemplateStruct """
        self.web_struct.command_line_interface = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                              question='Choose a command line library',
                                                                                              choices=['Click', 'Argparse', 'No command-line interface'],
                                                                                              default='Click',
                                                                                              dot_cookietemple=dot_cookietemple,
                                                                                              to_get_property='command_line_interface')
        self.web_struct.testing_library = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                       question='Choose a testing library',
                                                                                       choices=['pytest', 'unittest'],
                                                                                       default='pytest',
                                                                                       dot_cookietemple=dot_cookietemple,
                                                                                       to_get_property='testing_library')

    def web_prompt_github(self, dot_cookietemple) -> None:
        """
        Prompt for github repository creation when creating a web template
        :param dot_cookietemple: Dict (possibly empty) for a possible dry run
        """
        self.web_struct.is_github_repo, \
            self.web_struct.is_repo_private, \
            self.web_struct.is_github_orga, \
            self.web_struct.github_orga \
            = prompt_github_repo(dot_cookietemple)

    def website_django_options(self):
        click.echo(click.style('NOT YET IMPLEMENTED!', fg='red'))

    def handle_rest_api_python(self):
        click.echo(click.style('NOT YET IMPLEMENTED!', fg='red'))
