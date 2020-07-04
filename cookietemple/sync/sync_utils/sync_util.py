import os
from pathlib import Path
from packaging import version

from cookietemple.common.version import load_version, load_project_template_version_and_handle


def sync_load_template_version(handle: str) -> str:
    """
    Load the version of the template available from cookietemple specified by the handler for syncing.

    :param handle: The template handle
    :return: The actual version number of the template in cookietemple
    """
    top_path = f'{os.path.dirname(__file__)}/../..'
    available_templates_path = f'{str(top_path)}/create/templates/available_templates.yml'
    return load_version(handle, available_templates_path)


def sync_load_project_template_version_and_handle(project_dir: Path) -> str:
    """
    Return the project template version since last sync for user (if no sync happened, return initial create version of the template)

    :param project_dir: Top level path to users project directory
    """
    return load_project_template_version_and_handle(project_dir)


def has_template_version_changed(project_dir: Path) -> (bool, bool):
    """
    Check, if the cookietemple template has been updated since last check/sync of the user.

    :return: Both false if no versions changed or a micro change happened (for ex. 1.2.3 to 1.2.4). Return pr_major_change True if a major version release happened
    for the cookietemple template (for example 1.2.3 to 2.0.0). Return issue_minor_change True if a minor change happened (1.2.3 to 1.3.0).
    cookietemple will use this to decide which syncing strategy to apply.
    """
    template_version_last_sync, template_handle = sync_load_project_template_version_and_handle(project_dir)
    template_version_last_sync = version.parse(template_version_last_sync)
    actual_template_version = version.parse(sync_load_template_version(template_handle))
    pr_major_change = True if template_version_last_sync.major < actual_template_version.major else False
    issue_minor_change = True if template_version_last_sync.minor < actual_template_version.minor else False
    return pr_major_change, issue_minor_change
