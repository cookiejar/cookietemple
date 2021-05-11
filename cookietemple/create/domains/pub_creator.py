import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from rich import print

from cookietemple.common.version import load_ct_template_version
from cookietemple.config.config import ConfigCommand
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.create.github_support import load_github_username, prompt_github_repo
from cookietemple.create.template_creator import TemplateCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple


@dataclass
class TemplateStructPub(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for PUB projects
    """

    """
    This section contains some PUB-domain specific attributes
    """
    pubtype: str = ""
    author: str = ""
    title: str = ""
    university: str = ""
    department: str = ""
    degree: str = ""
    github_username = ""


class PubCreator(TemplateCreator):
    def __init__(self):
        self.pub_struct = TemplateStructPub(domain="pub", language="latex")
        super().__init__(self.pub_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_PUB_PATH = f"{self.WD_Path.parent}/templates/pub"

        '"" TEMPLATE VERSIONS ""'
        self.PUB_LATEX_TEMPLATE_VERSION = load_ct_template_version("pub-thesis-latex", self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, path: Path, dot_cookietemple: Optional[dict]):
        """
        Prompts the user for the publication type and forwards to subsequent prompts.
        Creates the pub template.
        """
        # latex is default language

        self.pub_struct.pubtype = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the following publication types",
            choices=["thesis"],
            dot_cookietemple=dot_cookietemple,
            to_get_property="pubtype",
        )

        if not os.path.exists(ConfigCommand.CONF_FILE_PATH):
            print("[bold red]Cannot find a Cookietemple config file! Is this your first time with Cookietemple?\n")
            print("[bold blue]Lets set your configs for Cookietemple and you are ready to go!\n")
            ConfigCommand.all_settings()

        # switch case statement to prompt the user to fetch template specific configurations
        switcher: Dict[str, Any] = {
            "latex": self.common_latex_options,
        }
        switcher.get(self.pub_struct.language.lower(), lambda: "Invalid language!")(dot_cookietemple)  # type: ignore

        self.handle_pub_type(dot_cookietemple)

        (
            self.pub_struct.is_github_repo,
            self.pub_struct.is_repo_private,
            self.pub_struct.is_github_orga,
            self.pub_struct.github_orga,
        ) = prompt_github_repo(dot_cookietemple)

        if self.pub_struct.is_github_orga:
            self.pub_struct.github_username = self.pub_struct.github_orga
        # create the pub template
        super().create_template_with_subdomain(self.TEMPLATES_PUB_PATH, self.pub_struct.pubtype)  # type: ignore

        # switch case statement to fetch the template version
        switcher_version = {
            "latex": self.PUB_LATEX_TEMPLATE_VERSION,
        }

        self.pub_struct.template_version = switcher_version.get(
            self.pub_struct.language.lower(), lambda: "Invalid language!"
        )
        self.pub_struct.template_version, self.pub_struct.template_handle = (
            switcher_version.get(self.pub_struct.language.lower(), lambda: "Invalid language!"),
            f"pub-{self.pub_struct.pubtype}-{self.pub_struct.language.lower()}",
        )

        # perform general operations like creating a GitHub repository and general linting, but skip common_files copying and rst linting
        super().process_common_operations(
            path=Path(path).resolve(),
            skip_common_files=True,
            skip_fix_underline=True,
            domain="pub",
            subdomain=self.pub_struct.pubtype,
            language=self.pub_struct.language,
            dot_cookietemple=dot_cookietemple,
        )

    def handle_pub_type(self, dot_cookietemple: Optional[dict]) -> None:
        """
        Determine the type of publication and handle it further.
        """

        switcher = {
            "thesis": self.handle_thesis_latex,
        }
        switcher.get(self.pub_struct.pubtype.lower(), lambda: "Invalid Pub Project Type!")(dot_cookietemple)  # type: ignore

    def handle_thesis_latex(self, dot_cookietemple: Optional[dict]) -> None:
        self.pub_struct.degree = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Degree",
            default="PhD",
            dot_cookietemple=dot_cookietemple,
            to_get_property="degree",
        )

    def common_latex_options(self, dot_cookietemple: Optional[dict]) -> None:
        """
        Prompt the user for common thesis/paper data
        """
        self.pub_struct.author = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Author",
            default="Homer Simpson",
            dot_cookietemple=dot_cookietemple,
            to_get_property="author",
        )
        self.pub_struct.project_slug = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Project name",
            default="PhD Thesis",
            dot_cookietemple=dot_cookietemple,
            to_get_property="project_name",
        ).replace(  # type: ignore
            " ", "_"
        )
        self.pub_struct.project_slug_no_hyphen = self.pub_struct.project_slug.replace("-", "_")
        self.pub_struct.title = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Publication title",
            default="On how Springfield exploded",
            dot_cookietemple=dot_cookietemple,
            to_get_property="title",
        )
        self.pub_struct.university = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="University",
            default="Homer J. Simpson University",
            dot_cookietemple=dot_cookietemple,
            to_get_property="university",
        )
        self.pub_struct.department = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Department",
            default="Department of Nuclear Physics",
            dot_cookietemple=dot_cookietemple,
            to_get_property="department",
        )
        self.pub_struct.github_username = load_github_username()  # Required for Github support
