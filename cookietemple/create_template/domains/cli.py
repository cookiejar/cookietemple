import os

import click
from cookiecutter.main import cookiecutter

import cookietemple.create_template.create as create

WD = os.path.dirname(__file__)

@click.command()
@click.option('--language',
              type=click.Choice(['C','C++','Kotlin'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_cli(language):
    create.TEMPLATE_STRUCT["language"] = language

    cookiecutter(f"{WD}/../../templates/cli_python")
