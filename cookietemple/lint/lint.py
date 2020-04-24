import os
import sys
from pathlib import Path
from subprocess import Popen, PIPE

import click
from ruamel.yaml import YAML

from cookietemple.lint.TemplateLinter import TemplateLinter
from cookietemple.lint.domains.cli import CliPythonLint
from cookietemple.lint.domains.web import WebWebsitePythonLint
from cookietemple.lint.domains.pub import PubLatexLint


def lint_project(project_dir: str, run_coala: bool = False, coala_interactive: bool = False) -> TemplateLinter:
    """
    Verifies the integrity of a project to best coding and practices.
    Runs coala (https://github.com/coala/coala) as a subprocess.
    """
    # Detect which template the project is based on
    template_handle = get_template_handle(project_dir)

    switcher = {
        'cli-python': CliPythonLint,
        'web-website-python': WebWebsitePythonLint,
        'pub-thesis-latex': PubLatexLint
    }

    lint_obj = switcher.get(template_handle, lambda: 'Invalid')(project_dir)
    # Run the linting tests
    try:
        # Disable check files?
        disable_check_files_templates = ['pub-thesis-latex']
        if template_handle in disable_check_files_templates:
            disable_check_files = True
        else:
            disable_check_files = False
        # Run non project specific linting
        click.echo(click.style('Running general linting', fg='blue'))
        lint_obj.lint_project(super(lint_obj.__class__, lint_obj), label='General Linting', custom_check_files=disable_check_files)

        # Run the project specific linting
        click.echo(click.style(f'Running {template_handle} linting', fg='blue'))
        lint_obj.lint(f'{template_handle} Linting')
    except AssertionError as e:
        click.echo(click.style(f'Critical error: {e}', fg='red'))
        click.echo(click.style(f'Stopping tests...', fg='red'))
        return lint_obj

    # Print the results
    lint_obj.print_results()

    # Exit code
    if len(lint_obj.failed) > 0:
        click.echo(click.style('Sorry, some tests failed - exiting with a non-zero error code...\n'))

    # Lint the project with Coala
    # A preconfigured .coa file should exist in the project, which is tested beforehand via linting
    if run_coala:
        call_coala(project_dir, coala_interactive)


def get_template_handle(dot_cookietemple_path: str = '.cookietemple.yml') -> str:
    """
    Reads the .cookietemple file and extracts the template handle
    :param dot_cookietemple_path: path to the .cookietemple file
    :return: found template handle
    """
    path = Path(f'{dot_cookietemple_path}/.cookietemple.yml')
    if not path.exists():
        click.echo(click.style('.cookietemple.yml not found. Is this a COOKIETEPLE project?', fg='red'))
        sys.exit(1)
    yaml = YAML(typ='safe')
    dot_cookietemple_content = yaml.load(path)

    return dot_cookietemple_content['template_handle']


def call_coala(path: str, interactive: bool) -> None:
    """
    Calls coala interactively as a subprocess.
    Verifies that coala is indeed installed.
    """
    if not is_coala_accessible():
        sys.exit(1)

    # We are calling coala as a subprocess, since it is not possible to run any of it's executable functions.
    # Coala has several interactive parts and therefore does not play nicely with our click setup.
    # (Leads to issues like 'lint' being passed as a parameter to coala), which it does of course not recognize.
    os.chdir(path)
    if interactive:
        coala = Popen(['coala'], universal_newlines=True, shell=False)
    else:
        coala = Popen(['coala', '--non-interactive'], universal_newlines=True, shell=False)
    (coala_stdout, coala_stderr) = coala.communicate()


def is_coala_accessible() -> bool:
    """
    Verifies that coala is accessible and in the PATH.

    :return: True if accessible, false if not
    """
    coala_installed = Popen(['git', '--version'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (coala_installed_stdout, coala_installed_stderr) = coala_installed.communicate()
    if coala_installed.returncode != 0:
        click.echo(click.style(f'Could not find \'coala\' in the PATH. Is it installed?', fg='red'))
        click.echo(click.style(f'Coala should have been installed with COOKIETEMPLE. Please use a virtual environment for COOKIETEMPLE', fg='blue'))
        click.echo(click.style('Run command was: coala', fg='red'))
        return False

    return True
