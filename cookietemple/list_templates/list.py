import click

@click.command()
@click.option('--list')
def list_all():
    print('Nix')
