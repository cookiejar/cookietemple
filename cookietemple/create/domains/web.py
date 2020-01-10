import os
import click
from cookietemple.create.create_config import (TEMPLATE_STRUCT,create_dot_cookietemple)

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['python', 'javaScript', 'erlang'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_web(language):
    TEMPLATE_STRUCT["language"] = language
    print(TEMPLATE_STRUCT)
