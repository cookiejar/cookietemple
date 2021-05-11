import logging
from pathlib import Path
from typing import Optional, Union

from cookietemple.create.domains.cli_creator import CliCreator
from cookietemple.create.domains.gui_creator import GuiCreator
from cookietemple.create.domains.lib_creator import LibCreator
from cookietemple.create.domains.pub_creator import PubCreator
from cookietemple.create.domains.web_creator import WebCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple

log = logging.getLogger(__name__)


def choose_domain(path: Path, domain: Union[str, bool], dot_cookietemple: Optional[dict]):
    """
    Prompts the user for the template domain.
    Creates the .cookietemple file.
    Prompts the user whether or not to create a Github repository

    :param domain: Template domain
    :param dot_cookietemple: Dictionary created from the .cookietemple.yml file. None if no .cookietemple.yml file was used.
    """
    if not domain:
        domain = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose the project's domain",
            choices=["cli", "lib", "gui", "web", "pub"],
            default="cli",
            dot_cookietemple=dot_cookietemple,
            to_get_property="domain",
        )

    switcher = {"cli": CliCreator, "web": WebCreator, "gui": GuiCreator, "lib": LibCreator, "pub": PubCreator}

    creator_obj: Union[CliCreator, WebCreator, GuiCreator, LibCreator, PubCreator] = switcher.get(domain.lower())()  # type: ignore
    creator_obj.create_template(path, dot_cookietemple)
