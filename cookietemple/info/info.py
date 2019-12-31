import click


@click.command()
@click.option('--info')
def info():
    print('List me baby')
