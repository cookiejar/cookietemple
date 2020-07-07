from collections import OrderedDict
from pathlib import Path

from ruamel.yaml import YAML

from cookietemple.create.create import choose_domain


def load_yaml_file(yaml_file_path: str) -> OrderedDict:
    """
    Loads a yaml file and returns the content as nested dictionary.

    :return: nested dictionary as the content of the yaml file
    """
    path = Path(yaml_file_path)
    yaml = YAML()
    return yaml.load(path)


def create_dry_template(dot_cookietemple: OrderedDict) -> None:
    choose_domain(domain=None, dot_cookietemple=dot_cookietemple)


create_dry_template(load_yaml_file('/home/zeth/PycharmProjects/cookietemple/cookietemple/sync/sync_test.yml'))