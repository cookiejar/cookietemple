import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from cookietemple.common.version import load_ct_template_version
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.create.github_support import prompt_github_repo
from cookietemple.create.template_creator import TemplateCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple


@dataclass
class TemplateStructGui(CookietempleTemplateStruct):
    """
    This class contains all attributes specific to GUI templates
    """

    id: str = ""
    organization: str = ""


class GuiCreator(TemplateCreator):
    def __init__(self):
        self.gui_struct = TemplateStructGui(domain="gui")
        super().__init__(self.gui_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_GUI_PATH = f"{self.WD_Path.parent}/templates/gui"

        '"" TEMPLATE VERSIONS ""'
        self.GUI_JAVA_TEMPLATE_VERSION = load_ct_template_version("gui-java", self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, path: Path, dot_cookietemple: Optional[Dict]):
        self.gui_struct.language = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the following languages",
            choices=["java"],
            dot_cookietemple=dot_cookietemple,
            to_get_property="language",
        )

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_cookietemple)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher: Dict[str, Any] = {
            "java": self.gui_java_options,
        }
        switcher.get(self.gui_struct.language.lower())(dot_cookietemple)  # type: ignore

        (
            self.gui_struct.is_github_repo,
            self.gui_struct.is_repo_private,
            self.gui_struct.is_github_orga,
            self.gui_struct.github_orga,
        ) = prompt_github_repo(dot_cookietemple)

        if self.gui_struct.is_github_orga:
            self.gui_struct.github_username = self.gui_struct.github_orga
        # create the gui template
        super().create_template_without_subdomain(self.TEMPLATES_GUI_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            "java": self.GUI_JAVA_TEMPLATE_VERSION,
        }

        self.gui_struct.template_version, self.gui_struct.template_handle = (
            switcher_version.get(self.gui_struct.language.lower()),  # type: ignore
            f"gui-{self.gui_struct.language.lower()}",  # type: ignore
        )  # type: ignore

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(
            path=Path(path).resolve(),
            domain="gui",
            language=self.gui_struct.language,
            dot_cookietemple=dot_cookietemple,
        )

    def gui_java_options(self, dot_cookietemple: Optional[Dict]) -> None:
        """
        Prompt the user for all gui-java specific properties
        """
        # The user id is automatically determined from the full_name as first letter of first name and sur name
        full_name_split = self.creator_ctx.full_name.split()  # type: ignore
        self.gui_struct.id = (
            f"{full_name_split[0][0]}{full_name_split[1][0]}"
            if len(full_name_split) > 1
            else f"{full_name_split[0][0]}"
        )
        self.gui_struct.organization = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Organization",
            default="organization",
            dot_cookietemple=dot_cookietemple,
            to_get_property="organization",
        )
