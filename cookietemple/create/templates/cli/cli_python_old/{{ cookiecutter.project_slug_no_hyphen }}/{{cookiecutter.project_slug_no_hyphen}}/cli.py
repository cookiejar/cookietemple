"""Console script for {{cookiecutter.project_slug}}."""
import os
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}
import sys
{%- if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}

from rich import traceback

WD = os.path.dirname(__file__)

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    read_included_file('test.txt')

    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main():
    """Console script for {{cookiecutter.project_slug}}."""
    read_included_file('test.txt')

    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")
    return 0
{%- endif %}

def read_included_file(filename):
    """
    DELETE ME

    This method solely demonstrates how to use and read files, which are automatically included in the distributed python package.
    @param filename: Name of the file to read, which has to be in a folder, that is included in the python package as specified in setup.py
    """
    print("function is called")
    with open(f"{WD}/files/{filename}") as f: content = f.readlines()
    print(content)

if __name__ == "__main__":
    traceback.install()
    sys.exit(main())  # pragma: no cover
