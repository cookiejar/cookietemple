import os
import click
import cookietemple.create_template.create as create

from cookiecutter.main import cookiecutter

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['python', 'c++', 'kotlin'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_cli(language):
    create.TEMPLATE_STRUCT["language"] = language

    cookiecutter(f"{TEMPLATES_PATH}/cli_python")

    create.create_dot_cookietemple(create.TEMPLATE_STRUCT)
