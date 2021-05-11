import sys
from pathlib import Path
from typing import Tuple

from rich import print

from cookietemple.common.load_yaml import load_yaml_file


def load_ct_template_version(handle: str, yaml_path: str) -> str:
    """
    Load the version of the template specified by the handler from the given yaml file path.

    :param handle: The template handle
    :param yaml_path: Path to the yaml file
    :return: The version number to the given handles template
    """
    available_templates = load_yaml_file(yaml_path)
    parts = handle.split("-")
    if len(parts) == 2:
        return available_templates[parts[0]][parts[1]]["version"]
    elif len(parts) == 3:

        return available_templates[parts[0]][parts[1]][parts[2]]["version"]

    return ""


def load_project_template_version_and_handle(project_dir: Path) -> Tuple[str, str]:
    """
    Load the template version when the user synced its project with cookietemple the last time.
    If no sync has been done so far, its the version of the cookietemple template the user created the project initially with.
    NOTE: This is NOT the projects current version (they are independent from each other)!!!

    :param project_dir: Top level directory of the users project.
    :return: The version number of the cookietemple template when the user created the project and the projects template handle.
    """
    try:
        ct_meta = load_yaml_file(f"{project_dir.__str__()}/.cookietemple.yml")
        # split the template version at first space to omit the cookietemple bump-version tag and return it and the handle
        return ct_meta["template_version"].split(" ", 1)[0], ct_meta["template_handle"]
    except FileNotFoundError:
        print(f"[bold red]No .cookietemple.yml found at {project_dir.__str__()}. Is this a cookietemple project?")
        sys.exit(1)
