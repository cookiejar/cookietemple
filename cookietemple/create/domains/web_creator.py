import os
from dataclasses import dataclass
from distutils.dir_util import copy_tree
from pathlib import Path
from shutil import copy
from typing import Any, Dict, Optional

from rich import print

from cookietemple.common.version import load_ct_template_version
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.create.github_support import prompt_github_repo
from cookietemple.create.template_creator import TemplateCreator
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.util.dir_util import delete_dir_tree


@dataclass
class TemplateStructWeb(CookietempleTemplateStruct):
    """
    This class contains all attributes specific for WEB projects
    This section contains some attributes specific for WEB-domain projects
    """

    webtype: str = ""  # the type of web project like website

    """
    General Python attributes
    """
    command_line_interface: str = ""  # which command line library to use (click, argparse)
    testing_library: str = ""  # which testing library to use (pytest, unittest)

    """
    This section contains some attributes specific for website projects
    """
    web_framework: str = ""  # the framework, the user wants to use (if any)
    setup_type: str = (
        ""  # indicates whether the user wants a basic website setup or a more advanced with database support etc.
    )
    use_frontend: str = ""  # indicates whether the user wants a shipped with frontend template or not
    frontend: str = ""  # the name of the frontend template (if any; the user has several options)
    url: str = ""  # the url for the website (if any)

    """
    This section contains some attributes specific for website projects
    """
    vmusername: str = ""  # the username (if any) for a VM (only necessary for Deployment in a Linux VM)


class WebCreator(TemplateCreator):
    def __init__(self):
        self.web_struct = TemplateStructWeb(domain="web")
        super().__init__(self.web_struct)
        self.WD_Path = Path(os.path.dirname(__file__))
        self.TEMPLATES_WEB_PATH = f"{self.WD_Path.parent}/templates/web"

        '""Web Template Versions""'
        self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION = load_ct_template_version(
            "web-website-python", self.AVAILABLE_TEMPLATES_PATH
        )

    def create_template(self, path: Path, dot_cookietemple: Optional[dict]) -> None:
        """
        Handles the Web domain. Prompts the user for the language, general and domain specific options.
        """
        self.web_struct.language = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the following languages",
            choices=["python"],
            default="python",
            dot_cookietemple=dot_cookietemple,
            to_get_property="language",
        )

        # prompt the user to fetch general template configurations
        super().prompt_general_template_configuration(dot_cookietemple)

        # switch case statement to prompt the user to fetch template specific configurations
        switcher: Dict[str, Any] = {
            "python": self.web_python_options,
        }
        switcher.get(self.web_struct.language)(dot_cookietemple)  # type: ignore
        # call handle function for specified language
        self.__getattribute__(f"handle_web_project_type_{self.web_struct.language}")(dot_cookietemple)
        # call handle function for specified webtype according to the chosen language
        self.__getattribute__(f"handle_{self.web_struct.webtype.lower()}_{self.web_struct.language}")(dot_cookietemple)
        # call option function for specified framework (if any)
        framework = self.web_struct.web_framework.lower()
        if framework:
            self.__getattribute__(f"{self.web_struct.webtype.lower()}_{framework}_options")(dot_cookietemple)

        (
            self.web_struct.is_github_repo,
            self.web_struct.is_repo_private,
            self.web_struct.is_github_orga,
            self.web_struct.github_orga,
        ) = prompt_github_repo(dot_cookietemple)
        # if repo owner is a github orga, update username
        if self.web_struct.is_github_orga:
            self.web_struct.github_username = self.web_struct.github_orga
        # create the project (TODO COOKIETEMPLE: As for now (only Flask) this works. Might need to change this in future.
        super().create_template_with_subdomain_framework(
            self.TEMPLATES_WEB_PATH, self.web_struct.webtype, self.web_struct.web_framework.lower()
        )
        # clean project for advanced or basic setup
        self.basic_or_advanced_files_with_frontend(self.web_struct.setup_type, self.web_struct.frontend.lower())

        # switch case statement to fetch the template version
        switcher_version = {"python": self.WEB_WEBSITE_PYTHON_TEMPLATE_VERSION}

        self.web_struct.template_version, self.web_struct.template_handle = (
            switcher_version.get(self.web_struct.language),  # type: ignore
            f"web-{self.web_struct.webtype}-{self.web_struct.language.lower()}",  # type: ignore
        )  # type: ignore

        # perform general operations like creating a GitHub repository and general linting
        super().process_common_operations(
            path=Path(path).resolve(),
            domain="web",
            subdomain=self.web_struct.webtype,
            language=self.web_struct.language,
            dot_cookietemple=dot_cookietemple,
        )

    def handle_web_project_type_python(self, dot_cookietemple: Optional[dict]) -> None:
        """
        Determine the type of web application
        """
        self.web_struct.webtype = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the following web domains",
            choices=["website"],
            default="website",
            dot_cookietemple=dot_cookietemple,
            to_get_property="webtype",
        )

    def handle_website_python(self, dot_cookietemple: Optional[dict]) -> None:
        """
        Handle the website template creation. The user can choose between a basic website setup and a more advanced
        with database support, mail, translation, cli commands for translation, login and register function.
        """
        self.web_struct.web_framework = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the following frameworks",
            choices=["flask"],
            default="flask",
            dot_cookietemple=dot_cookietemple,
            to_get_property="web_framework",
        )
        self.web_struct.setup_type = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose between the basic and advanced" " (database, translations, deployment scripts) template",
            choices=["basic", "advanced"],
            default="basic",
            dot_cookietemple=dot_cookietemple,
            to_get_property="setup_type",
        )

        self.web_struct.use_frontend = cookietemple_questionary_or_dot_cookietemple(
            function="confirm",
            question="Do you want to initialize your project" " with a advanced frontend template?",
            default="Yes",
            dot_cookietemple=dot_cookietemple,
            to_get_property="use_frontend",
        )

        # prompt the user for its frontend template, if he wants so
        if self.web_struct.use_frontend:
            print("[bold blue]The following templates are available:\n")

            # strings that start with https: are recognized by most terminal (emulators) as links
            print("[bold blue]https://html5up.net/solid-state")

            self.web_struct.frontend = cookietemple_questionary_or_dot_cookietemple(
                function="select",  # type: ignore
                question="Choose between the following predefined frontend templates",
                choices=["SolidState", "None"],
                dot_cookietemple=dot_cookietemple,
                to_get_property="frontend",
            ).lower()

        self.web_struct.url = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Project URL (if already existing)",
            default="dummy.com",
            dot_cookietemple=dot_cookietemple,
            to_get_property="url",
        )

    def website_flask_options(self, dot_cookietemple: Optional[dict]) -> None:
        """
        Prompt for flask template options
        """
        # prompt username for virtual machine (needed for example when deploying from a Linux VM)
        self.web_struct.vmusername = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Virtual machine username (if already existing)",
            default="cookietempleuser",
            dot_cookietemple=dot_cookietemple,
            to_get_property="vmusername",
        )

    def basic_or_advanced_files_with_frontend(self, setup_type: str, template_name: str) -> None:
        """
        Remove the dir/files that do not belong in a basic/advanced template and add a full featured frontend template
        if the user wants so.

        :param setup_type: Shows whether the user sets up a basic or advanced website setup
        :param template_name: the name of the frontend template (if any)
        """
        cwd = os.getcwd()
        os.chdir(f"{cwd}/{self.web_struct.project_slug_no_hyphen}/{self.web_struct.project_slug_no_hyphen}")

        # remove all stuff, that is not necessary for the basic setup
        if setup_type == "basic":
            delete_dir_tree(Path("translations"))
            delete_dir_tree(Path("auth"))
            delete_dir_tree(Path("main"))
            delete_dir_tree(Path("models"))
            delete_dir_tree(Path("services"))
            delete_dir_tree(Path("templates/auth"))
            os.remove("templates/index.html")
            os.remove("templates/base.html")
            os.remove("static/mail_stub.conf")
            os.remove("../babel.cfg")

            # the user wants only minimal frontend, so remove the index html file for this
            if not template_name or template_name == "none":
                os.remove("templates/basic_index_f.html")

        # remove basic stuff in advanced setup
        elif setup_type == "advanced":
            delete_dir_tree(Path("basic"))

        # the user wants to init its project with a full frontend
        if template_name and template_name != "none":
            copy_tree(f"../frontend_templates/{template_name}/assets", "static/assets")
            copy(f"../frontend_templates/{template_name}/index.html", "templates")

            # remove unnecessary files for basic frontend setup
            if setup_type == "basic":
                os.remove("templates/basic_index.html")
                os.remove("templates/index.html")
            # remove unnecessary files for advanced frontend setup
            else:
                os.remove("templates/basic_index_f.html")
                os.remove("templates/basic_index.html")

        else:
            # remove basic html files if advanced setup
            if setup_type == "advanced":
                os.remove("templates/basic_index.html")
                os.remove("templates/basic_index_f.html")

        # remove all frontend stuff
        delete_dir_tree(Path("../frontend_templates"))

        os.chdir(cwd)

    def web_python_options(self, dot_cookietemple: Optional[dict]):
        """ Prompts for web-python specific options and saves them into the CookietempleTemplateStruct """
        self.web_struct.command_line_interface = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose a command line library",
            choices=["Click", "Argparse", "No command-line interface"],
            default="Click",
            dot_cookietemple=dot_cookietemple,
            to_get_property="command_line_interface",
        )
        self.web_struct.testing_library = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose a testing library",
            choices=["pytest", "unittest"],
            default="pytest",
            dot_cookietemple=dot_cookietemple,
            to_get_property="testing_library",
        )
