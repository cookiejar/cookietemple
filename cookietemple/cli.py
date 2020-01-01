# -*- coding: utf-8 -*-

"""Entry point for cookietemple."""
import os
import sys
import click

from cookietemple.bump_version.bump_version import bump_version
from cookietemple.create_template.create import domain
from cookietemple.info.info import info
from cookietemple.linting import lint
from cookietemple.list.list import list_all

WD = os.path.dirname(__file__)


@click.command()
@click.option('--option',
              type=click.Choice(['Create', 'Lint', 'List', 'Info', 'Sync', 'Bump_version'], case_sensitive=False),
              prompt="Please choose from the following options")
def main(option):
    print(f"""
  / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
 / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \\ '_ ` _ \| '_ \| |/ _ \\
/ /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
\____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                               |_|
        """)

    from cookietemple.synchronization import sync
    switcher = {
        'create': domain,
        'lint': lint,
        'list': list_all,
        'info': info,
        'sync': sync,
        'bump_version': bump_version
    }

    switcher.get(option.lower(), lambda: 'Invalid')()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
