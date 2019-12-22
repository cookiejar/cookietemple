import click


@click.command()
@click.option('--lint')
def lint(lint):
    print(lint)
