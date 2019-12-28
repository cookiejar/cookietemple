import os
import click
#import cookietemple.create_template.pumpingercan as karleess
from cookietemple.create_template.pumpingercan import (TEMPLATE_STRUCT,create_dot_cookietemple)

from cookiecutter.main import cookiecutter

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['python', 'c++', 'kotlin'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_cli(language):
    TEMPLATE_STRUCT["language"] = language

    cookiecutter(f"{TEMPLATES_PATH}/cli_python")

    create_dot_cookietemple(TEMPLATE_STRUCT)
