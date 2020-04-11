from dataclasses import dataclass
from cookietemple.util.cookietemple_template_struct import CookietempleTemplateStruct


@dataclass
class TemplateStructWeb(CookietempleTemplateStruct):
    """
        This class contains all attributes specific for WEB projects
        """
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
