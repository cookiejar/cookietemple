import click
import yaml

from cookietemple.create_template.domains.cli import handle_cli
from cookietemple.create_template.domains.gui import handle_gui
from cookietemple.create_template.domains.web import handle_web

TEMPLATE_STRUCT = {}


@click.command()
@click.option('--domain',
              type=click.Choice(['CLI', 'GUI', 'Web'], case_sensitive=False),
              prompt="Choose between the following options")
def domain(domain):
    TEMPLATE_STRUCT["domain"] = domain
    switcher = {
        'cli': handle_cli,
        'web': handle_web,
        'gui': handle_gui
    }

    switcher.get(domain.lower(), lambda: 'Invalid')()

    create_dot_cookietemple(TEMPLATE_STRUCT)


def create_dot_cookietemple(TEMPLATE_STRUCT: dict):
    """
    Dumps the configuration for the template generation into a .cookietemple yaml file.

    @param TEMPLATE_STRUCT: global variable containing all cookietemple creation configuration variables
    """
    with open('.cookietemple', 'w') as f:
        yaml.dump(TEMPLATE_STRUCT, f)
