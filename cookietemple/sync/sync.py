import click
from cookietemple.sync.sync_utils.sync_util import sync_load_template_version


def snyc_template():
    click.echo(click.style(sync_load_template_version('cli-python'), fg='red'))
    click.echo(click.style(sync_load_template_version('web-website-python'), fg='red'))
    click.echo(click.style(sync_load_template_version('pub-thesis-latex'), fg='red'))
    click.echo(click.style(sync_load_template_version('cli-java'), fg='red'))
    click.echo(click.style(sync_load_template_version('gui-kotlin'), fg='red'))
    click.echo(click.style(sync_load_template_version('gui-java'), fg='red'))

