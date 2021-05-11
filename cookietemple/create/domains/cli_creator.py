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
class TemplateStructCli(CookietempleTemplateStruct):
    """
    CLI-PYTHON
    """

    command_line_interface: str = ""  # which command line library to use (click, argparse)
    testing_library: str = ""  # which testing library to use (pytest, unittest)

    """
    CLI-JAVA
    """
    group_domain: str = ""  # first part of groupID
    group_organization: str = ""  # second part of groupID
    main_class: str = ""  # name of the main class (determined from the capital project name)


class CliCreator(TemplateCreator):
    def __init__(self):
        self.cli_struct = TemplateStructCli(domain="cli")
        super().__init__(self.cli_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_CLI_PATH = f"{self.WD_Path.parent}/templates/cli"

        """ TEMPLATE VERSIONS """
        self.CLI_PYTHON_TEMPLATE_VERSION = load_ct_template_version("cli-python", self.AVAILABLE_TEMPLATES_PATH)
        self.CLI_JAVA_TEMPLATE_VERSION = load_ct_template_version("cli-java", self.AVAILABLE_TEMPLATES_PATH)

    def create_template(self, path: Path, dot_cookietemple: Optional[dict]):
        """
        Handles the CLI domain. Prompts the user for the language, general and domain specific options.
        """
        self.cli_struct.language = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose the project's primary language",
            choices=["python", "java"],
            default="python",
            dot_cookietemple=dot_cookietemple,
            to_get_property="language",
        )

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_cookietemple)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher: Dict[str, Any] = {
            "python": self.cli_python_options,
            "java": self.cli_java_options,
        }
        switcher.get(self.cli_struct.language)(dot_cookietemple)  # type: ignore

        (
            self.cli_struct.is_github_repo,
            self.cli_struct.is_repo_private,
            self.cli_struct.is_github_orga,
            self.cli_struct.github_orga,
        ) = prompt_github_repo(dot_cookietemple)

        if self.cli_struct.is_github_orga:
            self.cli_struct.github_username = self.cli_struct.github_orga
        # create the chosen and configured template
        super().create_template_without_subdomain(self.TEMPLATES_CLI_PATH)

        # switch case statement to fetch the template version
        switcher_version = {"python": self.CLI_PYTHON_TEMPLATE_VERSION, "java": self.CLI_JAVA_TEMPLATE_VERSION}
        self.cli_struct.template_version, self.cli_struct.template_handle = (
            switcher_version.get(self.cli_struct.language),  # type: ignore
            f"cli-{self.cli_struct.language.lower()}",  # type: ignore
        )

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(
            path=Path(path).resolve(),
            domain="cli",
            language=self.cli_struct.language,
            dot_cookietemple=dot_cookietemple,
        )

    def cli_python_options(self, dot_cookietemple: Optional[dict]):
        """
        Prompts for cli-python specific options and saves them into the CookietempleTemplateStruct
        """
        pass

    def cli_java_options(self, dot_cookietemple: Optional[dict]) -> None:
        """ Prompts for cli-java specific options and saves them into the CookietempleTemplateStruct """
        self.cli_struct.group_domain = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Domain (e.g. the org of org.apache)",
            default="com",
            dot_cookietemple=dot_cookietemple,
            to_get_property="group_domain",
        )
        self.cli_struct.group_organization = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Organization (e.g. the apache of org.apache)",
            default="organization",
            dot_cookietemple=dot_cookietemple,
            to_get_property="group_organization",
        )
        self.cli_struct.main_class = self.cli_struct.project_slug_no_hyphen.capitalize()
