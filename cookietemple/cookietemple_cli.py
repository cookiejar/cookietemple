# -*- coding: utf-8 -*-

'""Entry point for cookietemple.""'
import logging
import os
import sys
import click

from cookietemple.bump_version.bump_version import bump_template_version
from cookietemple.create.create import choose_domain
from cookietemple.info.info import show_info
from cookietemple.linting.lint import lint_project
from cookietemple.list.list import list_available_templates
from cookietemple.synchronization.sync import snyc_template
from cookietemple.util.click_util import CustomHelpOrder

WD = os.path.dirname(__file__)
COOKIETEMPLE_VERSION = '0.1.0'


def main():
    click.echo(click.style(f"""
      / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
     / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \\ '_ ` _ \| '_ \| |/ _ \\
    / /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
    \____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                                   |_|
        """, fg='blue'))

    click.echo(click.style('Run ', fg='green') + click.style('cookietemple --help ', fg='red')
               + click.style('for an overview of all commands', fg='green'))
    click.echo()

    cookietemple_cli()


@click.group(cls=CustomHelpOrder)
@click.version_option(COOKIETEMPLE_VERSION)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=False,
    help='Verbose output (print debug statements)'
)
def cookietemple_cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='\n%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='\n%(levelname)s: %(message)s')


@cookietemple_cli.command(help_priority=1)
@click.option('--domain',
              type=click.Choice(['CLI', 'GUI', 'Web'], case_sensitive=False))
def create(domain):
    """
    Create a new project using one of our templates

    """
    choose_domain(domain)


@cookietemple_cli.command(help_priority=2)
def lint():
    """
    Lint your existing COOKIETEMPLE project

    """
    lint_project()


@cookietemple_cli.command(help_priority=3)
def list():
    """
    List all available COOKIETEMPLE templates

    """
    list_available_templates()


@cookietemple_cli.command(help_priority=4)
@click.option('--handle',
              type=str)
def info(handle):
    """
    Get detailed info on a COOKIETEMPLE template

    """
    show_info(handle)


@cookietemple_cli.command(help_priority=5)
def sync():
    """
    Sync your project with the latest template release

    """
    snyc_template()


@cookietemple_cli.command(help_priority=6)
def bump_version():
    """
    Bump the version of an existing COOKIETEMPLE project

    """
    bump_template_version()


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
