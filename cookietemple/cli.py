# -*- coding: utf-8 -*-

"""Console script for cookietemple."""
import os
import sys
import click

WD = os.path.dirname(__file__)


@click.command()
def main(args=None):
    print(f"""


   ___            _    _      _                       _
  / __\___   ___ | | _(_) ___| |_ ___ _ __ ___  _ __ | | ___
 / /  / _ \ / _ \| |/ / |/ _ \ __/ _ \\ '_ ` _ \| '_ \| |/ _ \\
/ /__| (_) | (_) |   <| |  __/ ||  __/ | | | | | |_) | |  __/
\____/\___/ \___/|_|\_\_|\___|\__\___|_| |_| |_| .__/|_|\___|
                                               |_|



        """)
    with open(f"{WD}/templates/test.txt") as f: content = f.readlines()
    print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
