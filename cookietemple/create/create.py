from collections import OrderedDict

from cookietemple.create.domains.cli_creator import CliCreator
from cookietemple.create.domains.web_creator import WebCreator
from cookietemple.create.domains.gui_creator import GuiCreator
from cookietemple.create.domains.lib_creator import LibCreator
from cookietemple.create.domains.pub_creator import PubCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple


def choose_domain(domain: str or None, dot_cookietemple: OrderedDict = None, is_sync=False):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    :param dot_cookietemple: Dictionary created from the .cookietemple.yml file. None if no .cookietemple.yml file was used.
    """
    if not domain:
        domain = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                              question='Choose the project\'s domain',
                                                              choices=['cli', 'lib', 'gui', 'web', 'pub'],
                                                              default='cli',
                                                              dot_cookietemple=dot_cookietemple,
                                                              to_get_property='domain')

    switcher = {
        'cli': CliCreator,
        'web': WebCreator,
        'gui': GuiCreator,
        'lib': LibCreator,
        'pub': PubCreator
    }

    creator_obj = switcher.get(domain.lower())()
    creator_obj.create_template(dot_cookietemple, is_sync)
