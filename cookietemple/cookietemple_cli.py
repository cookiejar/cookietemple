# -*- coding: utf-8 -*-

"""Entry point for COOKIETEMPLE."""
import logging
import os
import sys

import click
import re
from pathlib import Path

import cookietemple

from cookietemple.bump_version.bump_version import bump_template_version
from cookietemple.create.create import choose_domain
from cookietemple.info.info import show_info
from cookietemple.lint.lint import lint_project
from cookietemple.list.list import list_available_templates
from cookietemple.package_dist.warp import warp_project
from cookietemple.synchronization.sync import snyc_template
from cookietemple.util.click_util import CustomHelpOrder

WD = os.path.dirname(__file__)


def main():
    click.echo(click.style(f"""
      / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
     / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \\ '_ ` _ \| '_ \| |/ _ \\
    / /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
    \____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                                   |_|
        """, fg='blue'))

    click.echo(click.style('Run ', fg='blue') + click.style('cookietemple --help ', fg='green') + click.style('for an overview of all commands', fg='blue'))
    click.echo()

    cookietemple_cli()


@click.group(cls=CustomHelpOrder)
@click.version_option(cookietemple.__version__,
                      message=click.style(f'Cookietemple Version: {cookietemple.__version__}', fg='blue'))
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=False,
    help='Verbose output (print debug statements)'
)
def cookietemple_cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@cookietemple_cli.command(help_priority=1, short_help='Create a new project using one of our templates.')
@click.option('--domain',
              type=click.Choice(['CLI', 'GUI', 'Web']))
def create(domain: str) -> None:
    """
    Create a new project using one of our templates

    """
    choose_domain(domain)


@cookietemple_cli.command(help_priority=2, short_help='Lint your existing COOKIETEMPLE project.')
@click.argument('project_dir', type=click.Path(),
                default=Path(f'{Path.cwd()}'))
@click.option('--run-coala/--no-run-coala',
              default=False)
def lint(project_dir, run_coala) -> None:
    """
    Lint your existing COOKIETEMPLE project
    """

    lint_project(project_dir, run_coala, True)


@cookietemple_cli.command(help_priority=3, short_help='List all available COOKIETEMPLE templates.')
def list() -> None:
    """
    List all available COOKIETEMPLE templates
    """

    list_available_templates()


@cookietemple_cli.command(help_priority=4, short_help='Get detailed info on a COOKIETEMPLE template domain or a single template.')
@click.argument('handle',
                type=str)
def info(handle: str) -> None:
    """
    Get detailed info on a COOKIETEMPLE template domain or a single template

    """
    show_info(handle)


@cookietemple_cli.command(help_priority=5, short_help='Sync your project with the latest template release.')
def sync() -> None:
    """
    Sync your project with the latest template release
    """

    snyc_template()


@cookietemple_cli.command('bump-version', help_priority=6, short_help='Bump the version of an existing COOKIETEMPLE project.')
@click.argument('new_version', type=str)
@click.argument('project_dir', type=click.Path(),
                default=Path(f'{Path.cwd()}'))
def bump_version(new_version, project_dir) -> None:
    """
    Bump the version of an existing COOKIETEMPLE project
    """

    if not new_version:
        click.echo(click.style('No new version specified.\nPlease specify a new version using '
                               '\'cookietemple bump_version my.new.version\'', fg='red'))
        sys.exit(0)

    elif not re.match(r"[0-9]+.[0-9]+.[0-9]+", new_version):
        click.echo(click.style('Invalid version specified!\nEnsure your version number has the form '
                               'like 0.0.0 or 15.100.239', fg='red'))
        sys.exit(0)

    elif not Path(f'{project_dir}/cookietemple.cfg').is_file():
        click.echo(click.style('Did not found a cookietemple.cfg file. Make sure you are in the right directory '
                               'or specify the path to your projects bump_version.cfg file', fg='red'))
        sys.exit(0)

    bump_template_version(new_version, project_dir)


@cookietemple_cli.command(help_priority=7, short_help='Create a self contained executable with bundled JRE.')
@click.option('--input_dir', type=str)
@click.option('--exec', type=str)
@click.option('--output', type=str)
def warp(input_dir: str, exec: str, output: str) -> None:
    """
    Create a self contained executable with bundled JRE
    """

    warp_project(input_dir, exec, output)


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
