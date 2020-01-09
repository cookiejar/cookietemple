# -*- coding: utf-8 -*-

"""Entry point for cookietemple."""
import os
import sys
import click

from cookietemple.bump_version.bump_version import bump_version
from cookietemple.create_template.create import domain
from cookietemple.info.info import info
from cookietemple.linting import lint
from cookietemple.list.list import list_available_templates
from cookietemple.synchronization import sync

WD = os.path.dirname(__file__)


def main():
    click.echo(click.style(f"""
      / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
     / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \\ '_ ` _ \| '_ \| |/ _ \\
    / /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
    \____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                                   |_|
        """, fg='blue'))

    click.echo(click.style('Run ', fg='green') + click.style('cookietemple --help ', fg='red') + click.style('for an overview of all commands', fg='green'))
    click.echo()

    determine_command()


@click.command()
@click.option('--command',
              type=click.Choice(['Create', 'Lint', 'List', 'Info', 'Sync', 'Bump_version'], case_sensitive=False),
              prompt="Please choose from the following options")
def determine_command(command):
    """ Cookietemple offers six distinct commands.

        \b
        create       -> Create a new Cookietemple template
        lint         -> Verify that your project follows best practices
        list         -> List all available templates
        info         -> Show detailed information about a specific template
        sync         -> Sync an existing project with the latest template release
        bump_version -> Conveniently bumps the version of an existing project
    """
    switcher = {
        'create': domain,
        'lint': lint,
        'list': list_available_templates,
        'info': info,
        'sync': sync,
        'bump_version': bump_version
    }

    switcher.get(command.lower(), lambda: 'Invalid')()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
