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
class TemplateStructLib(CookietempleTemplateStruct):
    """
    LIB-CPP
    """


class LibCreator(TemplateCreator):
    def __init__(self):
        self.lib_struct = TemplateStructLib(domain="lib")
        super().__init__(self.lib_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_LIB_PATH = f"{self.WD_Path.parent}/templates/lib"

        '"" TEMPLATE VERSIONS ""'
        self.LIB_CPP_TEMPLATE_VERSION = load_ct_template_version("lib-cpp", self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, path: Path, dot_cookietemple: Optional[dict]):
        """
        Handles the LIB domain. Prompts the user for the language, general and domain specific options.
        """

        self.lib_struct.language = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose the project's primary language",
            choices=["cpp"],
            default="cpp",
            dot_cookietemple=dot_cookietemple,
            to_get_property="language",
        )

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_cookietemple)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher: Dict[str, Any] = {
            "cpp": self.lib_cpp_options,
        }
        switcher.get(self.lib_struct.language)(dot_cookietemple)  # type: ignore

        (
            self.lib_struct.is_github_repo,
            self.lib_struct.is_repo_private,
            self.lib_struct.is_github_orga,
            self.lib_struct.github_orga,
        ) = prompt_github_repo(dot_cookietemple)

        if self.lib_struct.is_github_orga:
            self.lib_struct.github_username = self.lib_struct.github_orga
        # create the chosen and configured template
        super().create_template_without_subdomain(self.TEMPLATES_LIB_PATH)

        # switch case statement to fetch the template version
        switcher_version = {
            "cpp": self.LIB_CPP_TEMPLATE_VERSION,
        }
        self.lib_struct.template_version, self.lib_struct.template_handle = (
            switcher_version.get(self.lib_struct.language),  # type: ignore
            f"lib-{self.lib_struct.language.lower()}",  # type: ignore
        )  # type: ignore

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(
            path=Path(path).resolve(),
            domain="lib",
            language=self.lib_struct.language,
            dot_cookietemple=dot_cookietemple,
        )

    def lib_cpp_options(self, dot_cookietemple: Optional[Dict]):
        """ Prompts for lib-cpp specific options and saves them into the CookietempleTemplateStruct """
        pass
