from dataclasses import dataclass
from cookietemple.util.cookietemple_template_struct import CookietempleTemplateStruct


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
