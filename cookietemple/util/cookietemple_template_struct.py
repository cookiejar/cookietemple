from dataclasses import dataclass


@dataclass
class CookietempleTemplateStruct:
    """
    First section declares the variables that all template have in common
    """
    domain: str = ""  # the domain of the template: Currently available: CLI, WEB, GUI, PUB
    language: str = ""  # the language the project will be mainly written in
    project_slug: str = ""  # the project name Cookietemple uses for almost all further processing
    template_version: str = ""  # the version of the provided Cookietemple template
    template_handle: str = ""  # the handle of the specific template, indicating which template is currently used

    """
    This section contains some attributes common to the CLI, WEB and GUI domains
    """
    full_name: str = ""  # the name of the template creator/ the organization
    email: str = ""  # the email of the creator
    project_name: str = ""  # the projects name the template is created for
    project_short_description: str = ""  # a short description of the project
    version: str = ""  # the version of the project; of the form: [0-9]*\.[0-9]*\.[0-9]*
    license: str = ""  # the license of the project

    """
    This section contains some attributes specific for any python project
    """
    command_line_interface: str = ""  # the cmd line lib used, if any. TODO: Maybe this should go in common (as Java etc may also have this)
    use_pytest: str = ""  # indicates of the project wants to use pytest as the default testing framework

    """
    This section contains some attributes specific for WEB-domain projects 
    """
    # TODO: Currently only python but this will be refactored as we have more templates
    webtype: str = ""  # the type of web project like website or REST-API

    """
        This section contains some attributes specific for website projects
    """
    web_framework: str = ""  # the framework, the user wants to use (if any)
    is_basic_website: str = ""  # indicates whether the user wants a basic website setup or a more advanced with database support etc.
    url: str = ""  # the url for the website (if any)

    """
        This section contains some attributes specific for website projects
    """
    vm_username: str = ""  # the username (if any) for a VM (only necessary for Deployment in a Linux VM)

    """
    This section contains some PUB-domain specific attributes
    """
    pubtype: str = ""
    author: str = ""
    title: str = ""
    university: str = ""
    department: str = ""
    degree: str = ""
