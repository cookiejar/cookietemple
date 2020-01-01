import click

from cookietemple.create_template.create_config import (TEMPLATE_STRUCT, create_dot_cookietemple)
from cookietemple.create_template.domains.cli import handle_cli
from cookietemple.create_template.domains.gui import handle_gui
from cookietemple.create_template.domains.web import handle_web


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

    template_version = switcher.get(domain.lower(), lambda: 'Invalid')(standalone_mode=False)
    create_dot_cookietemple(TEMPLATE_STRUCT, template_version=template_version)
