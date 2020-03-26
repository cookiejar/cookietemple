import click

from cookietemple.create.create_config import (TEMPLATE_STRUCT)


def common_python_options():
    """
    Prompts for shared options of all python templates. Saves them in the TEMPLATE_STRUCT
    """
    TEMPLATE_STRUCT['command_line_interface'] = click.prompt('Choose a command line library:',
                                                             type=click.Choice(['Click', 'Argparse', 'No command-line interface']),
                                                             default='Click')
    testing_library = click.prompt('Please choose whether pytest or unittest should be used as the testing library [pytest, unittest]:',
                                   type=click.Choice(['pytest', 'unittest']),
                                   default='pytest')
    if testing_library == 'pytest':
        TEMPLATE_STRUCT['use_pytest'] = 'y'
    else:
        TEMPLATE_STRUCT['use_pytest'] = 'n'
