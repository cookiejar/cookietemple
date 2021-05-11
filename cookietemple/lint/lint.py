import logging
import sys
from pathlib import Path
from typing import Any, Optional, Union

from ruamel.yaml import YAML

from cookietemple.lint.domains.cli import CliJavaLint, CliPythonLint
from cookietemple.lint.domains.gui import GuiJavaLint
from cookietemple.lint.domains.lib import LibCppLint
from cookietemple.lint.domains.pub import PubLatexLint
from cookietemple.lint.domains.web import WebWebsitePythonLint
from cookietemple.lint.template_linter import TemplateLinter
from cookietemple.util.rich import console

log = logging.getLogger(__name__)


def lint_project(project_dir: str, skip_external: bool, is_create: bool = False) -> Optional[TemplateLinter]:
    """
    Verifies the integrity of a project to best coding and practices.
    Runs a set of general linting functions, which all templates share and afterwards runs template specific linting functions.
    All results are collected and presented to the user.

    :param project_dir: The path to the .cookietemple.yml file.
    :param skip_external: Whether to skip external linters such as autopep8
    :param is_create: Whether linting is called during project creation
    """
    # Detect which template the project is based on
    template_handle = get_template_handle(project_dir)
    log.debug(f"Detected handle {template_handle}")

    switcher = {
        "cli-python": CliPythonLint,
        "cli-java": CliJavaLint,
        "web-website-python": WebWebsitePythonLint,
        "gui-java": GuiJavaLint,
        "lib-cpp": LibCppLint,
        "pub-thesis-latex": PubLatexLint,
    }

    try:
        lint_obj: Union[TemplateLinter, Any] = switcher.get(template_handle)(project_dir)  # type: ignore
    except TypeError:
        console.print(f"[bold red]Unable to find linter for handle {template_handle}! Aborting...")
        sys.exit(1)

    # Run the linting tests
    try:
        # Disable check files?
        disable_check_files_templates = ["pub-thesis-latex"]
        if template_handle in disable_check_files_templates:
            disable_check_files = True
        else:
            disable_check_files = False
        # Run non project specific linting
        log.debug("Running general linting.")
        console.print("[bold blue]Running general linting")
        lint_obj.lint_project(
            super(lint_obj.__class__, lint_obj), custom_check_files=disable_check_files, is_subclass_calling=False
        )

        # Run the project specific linting
        log.debug(f"Running linting of {template_handle}")
        console.print(f"[bold blue]Running {template_handle} linting")

        # for every python project that is created autopep8 will run one time
        # when linting en existing python cookietemple project, autopep8 should be now optional,
        # since (for example) it messes up Jinja syntax (if included in project)
        if "python" in template_handle:
            lint_obj.lint(is_create, skip_external)  # type: ignore
        else:
            lint_obj.lint(skip_external)  # type: ignore
    except AssertionError as e:
        console.print(f"[bold red]Critical error: {e}")
        console.print("[bold red] Stopping tests...")
        return lint_obj

    # Print the results
    lint_obj.print_results()

    # Exit code
    if len(lint_obj.failed) > 0:
        console.print(f"[bold red] {len(lint_obj.failed)} tests failed! Exiting with non-zero error code.")
        sys.exit(1)

    return None


def get_template_handle(dot_cookietemple_path: str = ".cookietemple.yml") -> str:
    """
    Reads the .cookietemple file and extracts the template handle
    :param dot_cookietemple_path: path to the .cookietemple file
    :return: found template handle
    """
    path = Path(f"{dot_cookietemple_path}/.cookietemple.yml")
    if not path.exists():
        console.print("[bold red].cookietemple.yml not found. Is this a cookietemple project?")
        sys.exit(1)
    yaml = YAML(typ="safe")
    dot_cookietemple_content = yaml.load(path)

    return dot_cookietemple_content["template_handle"]
