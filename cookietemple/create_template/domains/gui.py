import os
import click
from cookietemple.create_template.create_config import (TEMPLATE_STRUCT)

WD = os.path.dirname(__file__)
TEMPLATES_PATH = f"{WD}/../templates"


@click.command()
@click.option('--language',
              type=click.Choice(['c++', 'c#', 'java'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_gui(language):
    TEMPLATE_STRUCT["language"] = language
    print(TEMPLATE_STRUCT)
