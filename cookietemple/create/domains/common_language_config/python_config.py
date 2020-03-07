import click

from cookietemple.create.create_config import (TEMPLATE_STRUCT)


def common_python_options():
    """
    # TODO
    """
    TEMPLATE_STRUCT['github_username'] = click.prompt('Please enter your Github account name (required for automatic deployment)',
                                                      type=str,
                                                      default='homersimpson')
    TEMPLATE_STRUCT['pypi_username'] = click.prompt('Please enter your pypi username (if you have one)',
                                                    type=str,
                                                    default='homersimpson')
    TEMPLATE_STRUCT['command_line_interface'] = click.prompt('Choose a command line library',
                                                             type=click.Choice(['Click', 'Argparse', 'No command-line interface']),
                                                             default='Click')
    testing_library = click.prompt('Please choose whether pytest or unittest should be used as the testing library [pytest, unittest]',
                                   type=click.Choice(['pytest', 'unittest']),
                                   default='pytest')
    if testing_library == 'pytest':
        TEMPLATE_STRUCT['use_pytest'] = 'y'
    else:
        TEMPLATE_STRUCT['use_pytest'] = 'n'
