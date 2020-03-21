import sys
from subprocess import Popen, PIPE

import click

from cookietemple.linting.TemplateLinter import TemplateLinter
from cookietemple.linting.domains.cli import CliPythonLint


def lint_project() -> TemplateLinter:
    """
    Verifies the integrity of a project to best coding and practices.
    Runs coala (https://github.com/coala/coala) as a subprocess.
    """
    # TODO Insert a switch statement here, which checks the .cookietemple file to decide which linter to apply next
    lint_obj = CliPythonLint()
    # Run the linting tests
    try:
        # Run non project specific linting
        lint_obj.lint_pipeline(super(lint_obj.__class__, lint_obj))
        lint_obj.lint_python()
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
    call_coala()


def call_coala() -> None:
    """
    Calls coala interactively as a subprocess.
    Verifies that coala is indeed installed.
    """
    if not is_coala_accessible():
        sys.exit(1)

    # We are calling coala as a subprocess, since it is not possible to run any of it's executable functions.
    # Coala has several interactive parts and therefore does not play nicely with our click setup.
    # (Leads to issues like 'lint' being passed as a parameter to coala), which it does of course not recognize.
    coala = Popen(['coala'], universal_newlines=True, shell=False)
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
