import click

import cookietemple.create_template.create as create


@click.command()
@click.option('--language',
              type=click.Choice(['Brainfuck','Racket', 'Julia'], case_sensitive=False),
              prompt="Choose between the following options:")
def handle_gui(language):
    create.TEMPLATE_STRUCT["language"] = language
    print(create.TEMPLATE_STRUCT)
