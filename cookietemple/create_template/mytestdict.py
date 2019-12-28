import yaml

TEMPLATE_STRUCT = {}

def create_dot_cookietemple(TEMPLATE_STRUCT: dict):
    """
    Dumps the configuration for the template generation into a .cookietemple yaml file.

    @param TEMPLATE_STRUCT: global variable containing all cookietemple creation configuration variables
    """
    with open('.cookietemple', 'w') as f:
        yaml.dump(TEMPLATE_STRUCT, f)
