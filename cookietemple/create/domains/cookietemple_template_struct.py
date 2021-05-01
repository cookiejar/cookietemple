from dataclasses import dataclass
from typing import Union


@dataclass
class CookietempleTemplateStruct:
    """
    First section declares the variables that all template have in common
    """

    cookietemple_version: str = ""  # Version of cookietemple, which was used for creating the project
    domain: str = ""  # Domain of the template
    language: str = ""  # Primary language
    project_slug: str = ""  # Project name cookietemple uses for almost all further processing
    project_slug_no_hyphen: str = (
        ""  # Required for some Python project specific things, since - don't play nice with Python
    )
    template_version: str = ""  # Version of the provided cookietemple template
    template_handle: str = ""  # Handle of the specific template, indicating which template is currently used
    github_username: str = ""  # Github username (in case of an organization repository, the organization name)
    creator_github_username: str = ""  # Github username of the person, that created the project
    is_github_repo: bool = False  # Whether the user wants to create a GitHub repo automatically
    is_repo_private: bool = False  # Whether to create a private Github repository
    is_github_orga: bool = False  # Whether Github repository is part of an organization
    github_orga: str = ""  # Name of the GitHub organization

    """
    This section contains some attributes common to cli, lib, gui, web
    """
    full_name: Union[str, bool] = ""  # Name of the template creator/organization
    email: Union[str, bool] = ""  # Email of the creator
    project_name: Union[str, bool] = ""  # Project's name the template is created for
    project_short_description: Union[str, bool] = ""  # A short description of the project
    version: Union[str, bool] = ""  # Version of the project; of the form: [0-9]*\.[0-9]*\.[0-9]*
    license: Union[str, bool] = ""  # License of the project
