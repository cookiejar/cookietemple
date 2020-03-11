from subprocess import Popen, PIPE

import click


def lint_project():
    """
    Verifies the integrity of a project to best coding and practices.
    Runs coala (https://github.com/coala/coala) as a subprocess.
    """

    call_coala()


def call_coala():
    """
    Calls coala interactively as a subprocess.
    Verifies that coala is indeed installed.
    :return:
    """
    if not is_coala_accessible():
        return

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
