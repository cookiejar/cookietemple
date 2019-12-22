import click

from cookietemple.create_template.domains.cli import handle_cli
from cookietemple.create_template.domains.gui import handle_gui
from cookietemple.create_template.domains.web import handle_web

TEMPLATE_STRUCT = {}


@click.command()
@click.option('--domain', type=click.Choice(['CLI','GUI','Web']),
              prompt="Choose between the following options")
def domain(domain):
    TEMPLATE_STRUCT["domain"] = domain
    switcher = {
        'cli': handle_cli,
        'web': handle_web,
        'gui': handle_gui
    }

    switcher.get(domain.lower(), lambda: 'Invalid')()
    print(domain)



