import os
import shutil

import click

from cookietemple.create.create_config import (TEMPLATE_STRUCT)
from cookietemple.create.create_templates import create_dot_cookietemple
from cookietemple.create.domains.cli import handle_cli
from cookietemple.create.domains.gui import handle_gui
from cookietemple.create.domains.web import handle_web
from cookietemple.create.github_support import create_push_github_repository
from cookietemple.linting.lint import lint_project

WD = os.path.dirname(__file__)
CWD = os.getcwd()


def choose_domain(domain: str):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    """
    if not domain:
        TEMPLATE_STRUCT['domain'] = click.prompt('Choose between the following domains [cli, gui, web]',
                                                 type=click.Choice(['cli', 'gui', 'web']))
    else:
        TEMPLATE_STRUCT['domain'] = domain

    switcher = {
        'cli': handle_cli,
        'web': handle_web,
        'gui': handle_gui
    }

    template_version, template_handle = switcher.get(TEMPLATE_STRUCT['domain'].lower(), lambda: 'Invalid')()
    create_dot_cookietemple(TEMPLATE_STRUCT, template_version=template_version, template_handle=template_handle)

    # Lint the project to verify that the new template adheres to all standards
    project_name = TEMPLATE_STRUCT['project_slug']
    project_path = f'{CWD}/{project_name}'
    lint_project(project_path, False)

    # ask user whether he wants to create a Github repository and do so if specified
    create_github_repository = click.prompt('Do you want to create a Github repository and push your template to it? [y, n]:',
                                            type=bool,
                                            default='Yes')
    if create_github_repository:
        tmp_project_path = f'{project_path}_cookietemple_tmp'
        # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
        os.rename(project_path, tmp_project_path)
        create_push_github_repository(project_name, 'some description', tmp_project_path)
        shutil.rmtree(tmp_project_path, ignore_errors=True)
