import os
import click
import cookietemple.create_template.pumpingercan as karleess

from cookiecutter.main import cookiecutter

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['python', 'c++', 'kotlin'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_cli(language):
    karleess.TEMPLATE_STRUCT["language"] = language

    cookiecutter(f"{TEMPLATES_PATH}/cli_python")

    karleess.create_dot_cookietemple(karleess.TEMPLATE_STRUCT)
