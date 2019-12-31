import click

@click.command()
@click.option('--bump_version')
def bump_version():
    print("Bump it")
