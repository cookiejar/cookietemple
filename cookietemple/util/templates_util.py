from pathlib import Path
from ruamel.yaml import YAML


def load_available_templates(available_templates_path: str) -> dict:
    """
    Loads 'available_templates.yaml' as a yaml file and returns the content as nested dictionary.

    :return: nested dictionary of all available templates
    """
    path = Path(available_templates_path)
    yaml = YAML(typ='safe')
    return yaml.load(path)
