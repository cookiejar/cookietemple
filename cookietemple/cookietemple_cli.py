# -*- coding: utf-8 -*-

"""Entry point for cookietemple."""
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
from cookietemple.upgrade.upgrade import UpgradeCommand
from cookietemple.warp.warp import warp_project
from cookietemple.custom_cli.custom_click import HelpErrorHandling, print_project_version, CustomHelpSubcommand, CustomArg
from cookietemple.config.config import ConfigCommand
from cookietemple.sync.sync import snyc_template

WD = os.path.dirname(__file__)


def main():
    traceback.install(width=200, word_wrap=True)
    click.echo(click.style(rf"""
      / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
     / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \ '_ ` _ \| '_ \| |/ _ \
    / /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
    \____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                                   |_|
        """, fg='blue'))

    click.echo(click.style('Run ', fg='blue') + click.style('cookietemple --help ', fg='green') + click.style('for an overview of all commands', fg='blue'))
    click.echo()

    # Is the latest cookietemple version installed? Upgrade if not!
    if not UpgradeCommand.check_cookietemple_latest():
        click.echo(click.style('Run ', fg='blue') + click.style('cookietemple upgrade ', fg='green') + click.style('to get the latest version.'))
    cookietemple_cli()


@click.group(cls=HelpErrorHandling)
@click.version_option(cookietemple.__version__, message=click.style(f'cookietemple Version: {cookietemple.__version__}', fg='blue'))
@click.option('-v', '--verbose', is_flag=True, default=False, help='Enable verbose output (print debug statements).')
@click.pass_context
def cookietemple_cli(ctx, verbose):
    """
    Create state of the art projects from production ready templates.
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@cookietemple_cli.command(short_help='Create a new project using one of our templates.', cls=CustomHelpSubcommand)
@click.option('--domain', type=click.Choice(['cli', 'lib', 'gui', 'web', 'pub']),
              help='The projects domain with currently cli, lib, gui, web and pub supported.')
def create(domain: str) -> None:
    """
    Create a new project using one of our templates.

    Creates a new project based on one of cookietemple's templates.
    You will be prompted for the domain, subdomain (if applicable), language and possibly framework.
    Template specific prompts follow. If you do not yet have a cookietemple config file you may be asked to create one first.
    Next, you will be asked whether you want to use cookietemple's Github support create a repository, push your template and enable a few settings.
    After the project has been created it will be linted and you will be notified of any TODOs.
    """
    choose_domain(domain)


@cookietemple_cli.command(short_help='Lint your existing cookietemple project.', cls=CustomHelpSubcommand)
@click.argument('project_dir', type=click.Path(), default=Path(str(Path.cwd())), helpmsg='Relative path to projects directory.', cls=CustomArg)
def lint(project_dir) -> None:
    """
    Lint your existing cookietemple project.

    Verify that your existing project still adheres to cookietemple's standards.
    cookietemple runs several general linting functions, which all templates share.
    Examples include a consistent project version, the existence of documentation and whether cookiecutter statements are still left.
    Afterwards, template specific linting is invoked. cli-python for example may check for the existence of a setup.py file.
    Both results are collected and displayed.
    """
    lint_project(project_dir)


@cookietemple_cli.command(short_help='List all available cookietemple templates.', cls=CustomHelpSubcommand)
def list() -> None:
    """
    List all available cookietemple templates.

    Get an overview of all existing cookietemple templates.
    The output only consists of a short description for all templates.
    To get a detailed overview of a specific subset of templates use info.
    """
    template_lister = TemplateLister()
    template_lister.list_available_templates()


@cookietemple_cli.command(short_help='Get detailed info on a cookietemple template domain or a single template.', cls=CustomHelpSubcommand)
@click.argument('handle', type=str, required=False, helpmsg='Language/domain of templates of interest.', cls=CustomArg)
@click.pass_context
def info(ctx, handle: str) -> None:
    """
    Get detailed info on a cookietemple template domain or a single template.

    list only provides an overview of all templates.
    Info provides a long description for a specific subset of templates.
    Pass a domain, language or full handle (e.g. cli-python).
    """
    if not handle:
        HelpErrorHandling.args_not_provided(ctx, 'info')
    else:
        template_info = TemplateInfo()
        template_info.show_info(handle.lower())


@cookietemple_cli.command(short_help='Sync your project with the latest template release.', cls=CustomHelpSubcommand)
@click.argument('project_dir', type=str, default=Path(f'{Path.cwd()}'), helpmsg='The projects top level directory you would like to sync. Default is current '
                                                                                'working directory.', cls=CustomArg)
def sync(project_dir) -> None:
    """
    Sync your project with the latest template release.

    cookietemple regularly updates its templates.
    To ensure that you have the latest changes you can invoke sync, which submits a pull request to your Github repository (if existing).
    If no repository exists the TEMPLATE branch will be updated and you can merge manually.
    """
    project_dir_path = Path(project_dir)
    snyc_template(project_dir_path)


@cookietemple_cli.command('bump-version', short_help='Bump the version of an existing cookietemple project.', cls=CustomHelpSubcommand)
@click.argument('new_version', type=str, required=False, helpmsg='New project version in a valid format.', cls=CustomArg)
@click.argument('project_dir', type=click.Path(), default=Path(f'{Path.cwd()}'), helpmsg='Relative path to the projects directory.', cls=CustomArg)
@click.option('--downgrade', '-d', is_flag=True, help='Set this flag to downgrade a version.')
@click.option('--project-version', is_flag=True, callback=print_project_version, expose_value=False, is_eager=True, help='Print your projects version and exit')
@click.pass_context
def bump_version(ctx, new_version, project_dir, downgrade) -> None:
    """
    Bump the version of an existing cookietemple project.

    INFO on valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
    version formats cookietemple allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
    separated by two dots.
    Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
    well as no substring of them will be recognized.

    Unless the user uses downgrade mode via the -d flag, a downgrade of a version is never allowed. Note that bump-version with the new version
    equals the current version is never allowed, either with or without -d.
    """
    if not new_version:
        HelpErrorHandling.args_not_provided(ctx, 'bump-version')
    else:
        # if the path entered ends with a trailing slash remove it for consistent output
        if str(project_dir).endswith('/'):
            project_dir = Path(str(project_dir).replace(str(project_dir)[len(str(project_dir)) - 1:], ''))

        version_bumper = VersionBumper(project_dir, downgrade)
        # lint before run bump-version
        version_bumper.lint_before_bump()
        # only run bump-version if conditions are met
        if version_bumper.can_run_bump_version(new_version, project_dir):
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


@cookietemple_cli.command(short_help='Create a self contained executable.', cls=CustomHelpSubcommand)
@click.option('--input_dir', type=str, required=True, help='Input directory.')
@click.option('--exec', type=str, required=True, help='Executable to package.')
@click.option('--output', type=str, required=True, help='Output directory.')
def warp(input_dir: str, exec: str, output: str) -> None:
    """
    Create a self contained executable.

    cookietemple bundles Warp (https://github.com/dgiagio/warp), which can be used to create self contained, native executables.
    Currently, cookietemple does not ship any templates, where this may be required.
    """
    warp_project(input_dir, exec, output)


@cookietemple_cli.command(short_help='Configure your general settings and github credentials.', cls=CustomHelpSubcommand)
@click.argument('section', type=str, required=False, helpmsg='Section to configure (all, general or pat)', cls=CustomArg)
@click.pass_context
def config(ctx, section: str) -> None:
    """
    Configure your general settings and Github credentials for reuse.
    Available options (sections) are:

    \b
    - general: set your fullname, email and Github username
    - pat: set your Github personal access token for Github repository creation
    - all: calls general and pat
    """
    if section == 'general':
        # set the full_name and email for reuse in the creation process
        ConfigCommand.config_general_settings()
    elif section == 'pat':
        # set github username and encrypted personal access token
        ConfigCommand.config_pat()
    elif section == 'all':
        # set everything
        ConfigCommand.all_settings()
        # empty section argument causes a customized error
    elif not section:
        HelpErrorHandling.args_not_provided(ctx, 'config')
        # check if a similar section handle can be used/suggested
    else:
        ConfigCommand.similar_handle(section)


@cookietemple_cli.command(short_help='Check for a newer version of cookietemple and upgrade if required.', cls=CustomHelpSubcommand)
def upgrade() -> None:
    """
    Checks whether the locally installed version of cookietemple is the latest.
    If not pip will be invoked to upgrade cookietemple to the latest version.
    """
    UpgradeCommand.check_upgrade_cookietemple()


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
