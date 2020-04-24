import click

from cookietemple.util.cookietemple_template_struct import CookietempleTemplateStruct


def common_python_options(creator_ctx: CookietempleTemplateStruct):
    """
    Prompts for shared options of all python templates. Saves them in the TEMPLATE_STRUCT
    """
    creator_ctx.command_line_interface = click.prompt('Choose a command line library:',
                                                      type=click.Choice(['Click', 'Argparse', 'No command-line interface']),
                                                      default='Click')
    creator_ctx.testing_library = click.prompt('Please choose whether pytest or unittest should be used as the testing library [pytest, unittest]:',
                                               type=click.Choice(['pytest', 'unittest']),
                                               default='pytest')
    if creator_ctx.testing_library == 'pytest':
        creator_ctx.use_pytest = 'y'
    else:
        creator_ctx.use_pytest = 'n'
