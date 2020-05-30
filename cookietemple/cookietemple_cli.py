# -*- coding: utf-8 -*-

"""Entry point for COOKIETEMPLE."""
import logging
import os
import sys
import click
from pathlib import Path
from rich import traceback

import cookietemple
from cookietemple.bump_version.bump_version import VersionBumper
from cookietemple.create.create import choose_domain
from cookietemple.info.info import TemplateInfo
from cookietemple.lint.lint import lint_project
from cookietemple.list.list import TemplateLister
from cookietemple.package_dist.warp import warp_project
from cookietemple.synchronization.sync import snyc_template
from cookietemple.custom_cookietemple_cli.custom_click import HelpErrorHandling, print_project_version

WD = os.path.dirname(__file__)


def main():
    traceback.install()
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


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'Current project version is {VersionBumper}')
    ctx.exit()


@click.group(cls=HelpErrorHandling)
@click.version_option(cookietemple.__version__, message=click.style(f'Cookietemple Version: {cookietemple.__version__}', fg='blue'))
@click.option('-v', '--verbose', is_flag=True, default=False, help='Verbose output (print debug statements)')
@click.pass_context
def cookietemple_cli(ctx, verbose):
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
                default=Path(str(Path.cwd())))
@click.option('--run-coala/--no-run-coala',
              default=False)
def lint(project_dir, run_coala) -> None:
    """
    Lint your existing COOKIETEMPLE project
    """
    lint_project(project_dir, run_coala, coala_interactive=True)


@cookietemple_cli.command(help_priority=3, short_help='List all available COOKIETEMPLE templates.')
def list() -> None:
    """
    List all available COOKIETEMPLE templates
    """
    template_lister = TemplateLister()
    template_lister.list_available_templates()


@cookietemple_cli.command(help_priority=4, short_help='Get detailed info on a COOKIETEMPLE template domain or a single template.')
@click.argument('handle', type=str, required=False)
@click.pass_context
def info(ctx, handle: str) -> None:
    """
    Get detailed info on a COOKIETEMPLE template domain or a single template
    """
    if not handle:
        HelpErrorHandling.args_not_provided(ctx, 'info')
    else:
        template_info = TemplateInfo()
        template_info.show_info(handle.lower())


@cookietemple_cli.command(help_priority=5, short_help='Sync your project with the latest template release.')
def sync() -> None:
    """
    Sync your project with the latest template release
    """
    snyc_template()


@cookietemple_cli.command('bump-version', help_priority=6, short_help='Bump the version of an existing COOKIETEMPLE project.')
@click.argument('new_version', type=str, required=False)
@click.argument('project_dir', type=click.Path(), default=Path(f'{Path.cwd()}'))
@click.option('--downgrade', '-d', is_flag=True)
@click.option('--project-version', is_flag=True, callback=print_project_version, expose_value=False, is_eager=True)
@click.pass_context
def bump_version(ctx, new_version, project_dir, downgrade) -> None:
    """
    Bump the version of an existing COOKIETEMPLE project

    INFO on valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
    version formats COOKIETEMPLE allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
    separated by two dots.
    Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
    well as no substring of them will be recognized.

    Unless the user indicates downgrade via he -d flag, a downgrade of a version is never allowed. Note that bump-version with the new version
    equals the current version is never allowed, either with or without -d.
    """
    if not new_version:
        HelpErrorHandling.args_not_provided(ctx, 'bump-version')
    else:
        # if the path entered ends with a trailing slash remove it for consistent output
        if str(project_dir).endswith('/'):
            project_dir = Path(str(project_dir).replace(str(project_dir)[len(str(project_dir)) - 1:], ''))

        version_bumper = VersionBumper(project_dir)

        if version_bumper.can_run_bump_version(new_version, project_dir, downgrade):
            # only run "sanity" checker when the downgrade flag is not set
            if not downgrade:
                # if the check fails, ask the user for confirmation
                if version_bumper.check_bump_range(version_bumper.CURRENT_VERSION.split('-')[0], new_version.split('-')[0]):
                    version_bumper.bump_template_version(new_version, project_dir)
                elif click.confirm(click.style(f'Bumping from {version_bumper.CURRENT_VERSION} to {new_version} seems not reasonable.\n'
                                               f'Do you really want to bump the project version?', fg='blue')):
                    click.echo('\n')
                    version_bumper.bump_template_version(new_version, project_dir)
            else:
                version_bumper.bump_template_version(new_version, project_dir)

        else:
            sys.exit(1)


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
