import logging

import click

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("cookietemple create")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

def bump_template_version():
    click.echo(click.style('NOT IMPLEMENTED YET', fg='red'))
