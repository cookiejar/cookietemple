import logging

import click

from cookietemple.create.create_config import (TEMPLATE_STRUCT, create_dot_cookietemple)
from cookietemple.create.domains.cli import handle_cli
from cookietemple.create.domains.gui import handle_gui
from cookietemple.create.domains.web import handle_web

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("cookietemple create")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def choose_domain(domain):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.

    :param domain: Template domain
    """
    if not domain:
        TEMPLATE_STRUCT['domain'] = click.prompt('Choose between the following domains',
                                                 type=click.Choice(['CLI', 'GUI', 'Web'], case_sensitive=False))
    else:
        TEMPLATE_STRUCT['domain'] = domain

    switcher = {
        'cli': handle_cli,
        'web': handle_web,
        'gui': handle_gui
    }

    template_version, template_handle = switcher.get(TEMPLATE_STRUCT["domain"].lower(), lambda: 'Invalid')()
    create_dot_cookietemple(TEMPLATE_STRUCT, template_version=template_version, template_handle=template_handle)
