"""Console script for cookietemple."""
import os
import sys
import click

from rich import traceback

WD = os.path.dirname(__file__)


@click.command()
def main(args=None):
    """Console script for cookietemple."""
    read_included_file('test.txt')

    click.echo("Replace this message by putting your code into "
               "cookietemple.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


def read_included_file(filename):
    """
    DELETE ME

    This method solely demonstrates how to use and read files, which are automatically included in the distributed python package.
    @param filename: Name of the file to read, which has to be in a folder, that is included in the python package as specified in setup.py
    """
    print("function is called")
    with open(f"{WD}/files/{filename}") as f:
        content = f.readlines()
    print(content)


if __name__ == "__main__":
    traceback.install()
    sys.exit(main())  # pragma: no cover
