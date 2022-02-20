import logging
import os
import re
import shutil
import sys
import tempfile
from dataclasses import asdict
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Optional, Union

import requests
from cookiecutter.main import cookiecutter  # type: ignore
from ruamel.yaml import YAML

import cookietemple
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.config.config import ConfigCommand
from cookietemple.create.domains.cookietemple_template_struct import CookietempleTemplateStruct
from cookietemple.create.github_support import create_push_github_repository, is_git_repo, load_github_username
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.lint.lint import lint_project
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.util.docs_util import fix_short_title_underline
from cookietemple.util.rich import console

log = logging.getLogger(__name__)


class TemplateCreator:
    """
    The base class for all creators.
    It holds the basic template information that are common across all templates (like a project name).
    Furthermore it defines methods that are basic for the template creation process.
    """

    def __init__(self, creator_ctx: CookietempleTemplateStruct):
        self.WD = os.path.dirname(__file__)
        self.TEMPLATES_PATH = f"{self.WD}/templates"
        self.COMMON_FILES_PATH = f"{self.TEMPLATES_PATH}/common_files"
        self.AVAILABLE_TEMPLATES_PATH = f"{self.TEMPLATES_PATH}/available_templates.yml"
        self.AVAILABLE_TEMPLATES = load_yaml_file(self.AVAILABLE_TEMPLATES_PATH)
        self.CWD = Path.cwd()
        self.creator_ctx = creator_ctx

    def process_common_operations(
        self,
        path: Path,
        skip_common_files=False,
        skip_fix_underline=False,
        domain: Optional[str] = None,
        subdomain: Union[str, bool] = None,
        language: Union[str, bool] = None,
        dot_cookietemple: Optional[dict] = None,
    ) -> None:
        """
        Create all stuff that is common for cookietemples template creation process; in detail those things are:
        create and copy common files, fix docs style, lint the project and ask whether the user wants to create a github repo.
        """
        # create the common files and copy them into the templates directory (skip if flag is set)

        if not skip_common_files:
            self.create_common_files()

        self.create_dot_cookietemple(template_version=self.creator_ctx.template_version)

        if self.creator_ctx.language == "python":
            project_path = f'{self.CWD}/{self.creator_ctx.project_slug.replace("-", "_")}'
        else:
            project_path = f"{self.CWD}/{self.creator_ctx.project_slug}"

        # Ensure that docs are looking good (skip if flag is set)
        if not skip_fix_underline:
            fix_short_title_underline(f"{project_path}/docs/index.rst")

        # Lint the project to verify that the new template adheres to all standards
        lint_project(project_path)

        if self.creator_ctx.is_github_repo and not dot_cookietemple:
            # rename the currently created template to a temporary name, create Github repo, push, remove temporary template
            tmp_project_path = f"{project_path}_cookietemple_tmp"
            os.mkdir(tmp_project_path)
            create_push_github_repository(project_path, self.creator_ctx, tmp_project_path)
            shutil.rmtree(tmp_project_path, ignore_errors=True)

        if subdomain:
            console.print()
            console.print(
                "[bold blue]Please visit: https://cookietemple.readthedocs.io/en/latest/available_templates/available_templates.html"
                f"#{domain}-{subdomain}-{language} for more information about how to use your chosen template."
            )
        else:
            console.print()
            console.print(
                "[bold blue]Please visit: https://cookietemple.readthedocs.io/en/latest/available_templates/available_templates.html"
                f"#{domain}-{language} for more information about how to use your chosen template."
            )

        # do not move if path is current working directory or a directory named like the project in the current working directory (second is default case)
        if path != self.CWD and path != Path(self.CWD / self.creator_ctx.project_slug_no_hyphen):
            shutil.move(
                f"{self.CWD}/{self.creator_ctx.project_slug_no_hyphen}",
                f"{path}/{self.creator_ctx.project_slug_no_hyphen}",
            )

    def create_template_without_subdomain(self, domain_path: str) -> None:
        """
        Creates a chosen template that does **not** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        """
        # Target directory is already occupied -> overwrite?
        occupied = os.path.isdir(f"{self.CWD}/{self.creator_ctx.project_slug}")
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary_or_dot_cookietemple("confirm", "Do you really want to continue?", default="No"):
                cookiecutter(
                    f"{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}",
                    no_input=True,
                    overwrite_if_exists=True,
                    extra_context=self.creator_ctx_to_dict(),
                )
            else:
                console.print("[bold red]Aborted! Canceled template creation!")
                sys.exit(0)
        else:
            cookiecutter(
                f"{domain_path}/{self.creator_ctx.domain}_{self.creator_ctx.language.lower()}",
                no_input=True,
                overwrite_if_exists=True,
                extra_context=self.creator_ctx_to_dict(),
            )

    def create_template_with_subdomain(self, domain_path: str, subdomain: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        """
        occupied = os.path.isdir(f"{self.CWD}/{self.creator_ctx.project_slug}")
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary_or_dot_cookietemple(
                "confirm", "Do you really want to continue?", default="Yes"
            ):
                delete_dir_tree(Path(f"{self.CWD}/{self.creator_ctx.project_slug}"))
                cookiecutter(
                    f"{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}",
                    no_input=True,
                    overwrite_if_exists=True,
                    extra_context=self.creator_ctx_to_dict(),
                )

            else:
                console.print("[bold red]Aborted! Canceled template creation!")
                sys.exit(0)
        else:
            cookiecutter(
                f"{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}",
                no_input=True,
                overwrite_if_exists=True,
                extra_context=self.creator_ctx_to_dict(),
            )

    def create_template_with_subdomain_framework(self, domain_path: str, subdomain: str, framework: str) -> None:
        """
        Creates a chosen template that **does** have a subdomain.
        Calls cookiecutter on the main chosen template.

        :param domain_path: Path to the template, which is still in cookiecutter format
        :param subdomain: Subdomain of the chosen template
        :param framework: Chosen framework
        """
        occupied = os.path.isdir(f"{self.CWD}/{self.creator_ctx.project_slug}")
        if occupied:
            self.directory_exists_warning()

            # Confirm proceeding with overwriting existing directory
            if cookietemple_questionary_or_dot_cookietemple(
                "confirm", "Do you really want to continue?", default="Yes"
            ):
                cookiecutter(
                    f"{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}",
                    no_input=True,
                    overwrite_if_exists=True,
                    extra_context=self.creator_ctx_to_dict(),
                )

            else:
                console.print("[bold red]Aborted! Canceled template creation!")
                sys.exit(0)
        else:
            cookiecutter(
                f"{domain_path}/{subdomain}_{self.creator_ctx.language.lower()}/{framework}",
                no_input=True,
                overwrite_if_exists=True,
                extra_context=self.creator_ctx_to_dict(),
            )

    def prompt_general_template_configuration(self, dot_cookietemple: Optional[dict]):
        """
        Prompts the user for general options that are required by all templates.
        Options are saved in the creator context manager object.
        """
        try:
            """
            Check, if the dot_cookietemple dictionary contains the full name and email (this happens, when dry creating the template while syncing on
            TEMPLATE branch).
            If that's not the case, try to read them from the config file (created with the config command).

            If none of the approaches above succeed (no config file has been found and its not a dry create run), configure the basic credentials and proceed.
            """
            if dot_cookietemple:
                self.creator_ctx.full_name = dot_cookietemple["full_name"]
                self.creator_ctx.email = dot_cookietemple["email"]
            else:
                self.creator_ctx.full_name = load_yaml_file(ConfigCommand.CONF_FILE_PATH)["full_name"]
                self.creator_ctx.email = load_yaml_file(ConfigCommand.CONF_FILE_PATH)["email"]
        except FileNotFoundError:
            # style and automatic use config
            console.print(
                "[bold red]Cannot find a cookietemple config file. Is this your first time using cookietemple?"
            )
            # inform the user and config all settings (with PAT optional)
            console.print("[bold blue]Lets set your name, email and Github username and you´re ready to go!")
            ConfigCommand.all_settings()
            # load mail and full name
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML(typ="safe")
            settings = yaml.load(path)
            # set full name and mail
            self.creator_ctx.full_name = settings["full_name"]
            self.creator_ctx.email = settings["email"]

        self.creator_ctx.project_name = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Project name",
            default="exploding-springfield",
            dot_cookietemple=dot_cookietemple,
            to_get_property="project_name",
        ).lower()  # type: ignore
        if self.creator_ctx.language == "python":
            self.check_name_available("PyPi", dot_cookietemple)
        self.check_name_available("readthedocs.io", dot_cookietemple)
        self.creator_ctx.project_slug = self.creator_ctx.project_name.replace(" ", "_")  # type: ignore
        self.creator_ctx.project_slug_no_hyphen = self.creator_ctx.project_slug.replace("-", "_")
        self.creator_ctx.project_short_description = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Short description of your project",
            default=f"{self.creator_ctx.project_name}" f". A cookietemple based .",
            dot_cookietemple=dot_cookietemple,
            to_get_property="project_short_description",
        )
        poss_vers = cookietemple_questionary_or_dot_cookietemple(
            function="text",
            question="Initial version of your project",
            default="0.1.0",
            dot_cookietemple=dot_cookietemple,
            to_get_property="version",
        )

        # make sure that the version has the right format
        while not re.match(r"(?<!.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!.)", poss_vers) and not dot_cookietemple:  # type: ignore
            console.print(
                "[bold red]The version number entered does not match semantic versioning.\n"
                + r"Please enter the version in the format \[number].\[number].\[number]!"
            )  # noqa: W605
            poss_vers = cookietemple_questionary_or_dot_cookietemple(
                function="text", question="Initial version of your project", default="0.1.0"
            )
        self.creator_ctx.version = poss_vers

        self.creator_ctx.license = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="License",
            choices=[
                "MIT",
                "BSD",
                "ISC",
                "Apache2.0",
                "GNUv3",
                "Boost",
                "Affero",
                "CC0",
                "CCBY",
                "CCBYSA",
                "Eclipse",
                "WTFPL",
                "unlicence",
                "Not open source",
            ],
            default="MIT",
            dot_cookietemple=dot_cookietemple,
            to_get_property="license",
        )
        if dot_cookietemple:
            self.creator_ctx.github_username = dot_cookietemple["github_username"]
            self.creator_ctx.creator_github_username = dot_cookietemple["creator_github_username"]
        else:
            self.creator_ctx.github_username = load_github_username()
            self.creator_ctx.creator_github_username = self.creator_ctx.github_username

    def create_common_files(self) -> None:
        """
        Create a temporary directory for common files of all templates and apply cookiecutter on them.
        They are subsequently moved into the directory of the created template.
        """
        log.debug("Creating common files.")
        dirpath = tempfile.mkdtemp()
        copy_tree(f"{self.COMMON_FILES_PATH}", dirpath)
        cwd_project = self.CWD
        os.chdir(dirpath)
        log.debug(f"Cookiecuttering common files at {dirpath}")
        cookiecutter(
            dirpath,
            extra_context={
                "full_name": self.creator_ctx.full_name,
                "email": self.creator_ctx.email,
                "language": self.creator_ctx.language,
                "domain": self.creator_ctx.domain,
                "project_name": self.creator_ctx.project_name,
                "project_slug": self.creator_ctx.project_slug
                if self.creator_ctx.language != "python"
                else self.creator_ctx.project_slug_no_hyphen,
                "version": self.creator_ctx.version,
                "license": self.creator_ctx.license,
                "project_short_description": self.creator_ctx.project_short_description,
                "github_username": self.creator_ctx.github_username,
                "creator_github_username": self.creator_ctx.creator_github_username,
                "cookietemple_version": cookietemple.__version__,
            },
            no_input=True,
            overwrite_if_exists=True,
        )

        # recursively copy the common files directory content to the created project
        log.debug("Copying common files into the created project")
        dest_dir = (
            self.creator_ctx.project_slug
            if self.creator_ctx.language != "python"
            else self.creator_ctx.project_slug_no_hyphen
        )
        copy_tree(f"{Path.cwd()}/common_files_util", f"{cwd_project}/{dest_dir}")
        # delete the tmp cookiecuttered common files directory
        log.debug("Delete common files directory.")
        delete_dir_tree(Path(f"{Path.cwd()}/common_files_util"))
        try:
            shutil.rmtree(dirpath)
        except PermissionError:
            # If deleting these temporary files fails, fail silently (#748)
            pass
        # change to recent cwd so lint etc can run properly
        os.chdir(str(cwd_project))

    def check_name_available(self, host, dot_cookietemple) -> None:
        """
        Main function that calls the queries for the project name lookup at PyPi and readthedocs.io
        """
        # if project already exists at either PyPi or readthedocs, ask user for confirmation with the option to change the project name
        while TemplateCreator.query_name_available(host, self.creator_ctx.project_name) and not dot_cookietemple:  # type: ignore
            console.print(f"[bold red]A project named {self.creator_ctx.project_name} already exists at {host}!")
            # provide the user an option to change the project's name
            if cookietemple_questionary_or_dot_cookietemple(
                function="confirm",
                question="Do you want to choose another name for your project?\n"
                f"Otherwise you will not be able to host your project at {host}!",
                default="Yes",
            ):
                self.creator_ctx.project_name = cookietemple_questionary_or_dot_cookietemple(
                    function="text", question="Project name", default="Exploding Springfield"
                )
            # continue if the project should be named anyways
            else:
                break

    @staticmethod
    def query_name_available(host: str, project_name: str) -> bool:
        """
        Make a GET request to the host to check whether a project with this name already exists.
        :param host The host (either PyPi or readthedocs)
        :param project_name Name of the project the user wants to create

        :return: Whether request was successful (name already taken on host) or not
        """
        # check if host is either PyPi or readthedocs.io; only relevant for developers working on this code
        if host not in {"PyPi", "readthedocs.io"}:
            log.debug(f"[bold red]Unknown host {host}. Use either PyPi or readthedocs.io!")
            # raise a ValueError if the host name is invalid
            raise ValueError(
                f"check_name_available has been called with the invalid host {host}.\nValid hosts are PyPi and readthedocs.io"
            )
        console.print(f"[bold blue]Looking up {project_name} at {host}!")
        # determine url depending on host being either PyPi or readthedocs.io
        url = "https://" + (
            f'pypi.org/project/{project_name.replace(" ", "")}'
            if host == "PyPi"
            else f'{project_name.replace(" ", "")}.readthedocs.io'
        )
        log.debug(f"Looking up {url}")
        try:
            request = requests.get(url)
            if request.status_code == 200:
                return True
        # catch exceptions when server may be unavailable or the request timed out
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            log.debug(f"Unable to contact {host}")
            log.debug(f"Error was: {e}")
            console.print(
                f"[bold red]Cannot check whether name already taken on {host} because its unreachable at the moment!"
            )
            return False

        return False

    def directory_exists_warning(self) -> None:
        """
        If the directory is already a git directory within the same project, print error message and exit.
        Otherwise print a warning that a directory already exists and any further action on the directory will overwrite its contents.
        """
        if is_git_repo(Path(f"{self.CWD}/{self.creator_ctx.project_slug}")):
            console.print(
                f"[bold red]Error: A git project named {self.creator_ctx.project_slug} already exists at [green]{self.CWD}\n"
            )
            console.print("[bold red]Aborting!")
            sys.exit(1)
        else:
            console.print(
                f"[bold yellow]WARNING: [red]A directory named {self.creator_ctx.project_slug} already exists at [blue]{self.CWD}\n"
            )
            console.print("Proceeding now will overwrite this directory and its content!")

    def create_dot_cookietemple(self, template_version: str):
        """
        Overrides the version with the version of the template.
        Dumps the configuration for the template generation into a .cookietemple yaml file.

        :param template_version: Version of the specific template
        """
        log.debug("Creating .cookietemple.yml file.")
        self.creator_ctx.template_version = f"{template_version} # <<COOKIETEMPLE_NO_BUMP>>"
        self.creator_ctx.cookietemple_version = f"{cookietemple.__version__} # <<COOKIETEMPLE_NO_BUMP>>"
        # Python does not allow for hyphens (module imports etc) -> remove them
        no_hyphen = self.creator_ctx.project_slug.replace("-", "_")
        with open(
            f'{self.creator_ctx.project_slug if self.creator_ctx.language != "python" else no_hyphen}/.cookietemple.yml',
            "w",
        ) as f:
            yaml = YAML()
            struct_to_dict = self.creator_ctx_to_dict()
            yaml.dump(struct_to_dict, f)

    def creator_ctx_to_dict(self) -> dict:
        """
        Create a dict from the our Template Structure dataclass
        :return: The dict containing all key-value pairs with non empty values
        """
        return {key: val for key, val in asdict(self.creator_ctx).items() if val != ""}
