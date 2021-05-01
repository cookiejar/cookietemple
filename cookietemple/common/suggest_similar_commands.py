import os
from typing import Set

from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.util.dict_util import is_nested_dictionary

AVAILABLE_TEMPLATES_PATH = f"{os.path.dirname(__file__)}/../create/templates/available_templates.yml"

# cookietemple's main commands
MAIN_COMMANDS = ["create", "lint", "list", "info", "bump-version", "sync", "warp", "config", "upgrade"]
# the fraction relative to the commands length, a given input could differ from the real command to be automatically used instead
SIMILARITY_USE_FACTOR = 1 / 3
# the fraction relative to the commands length, a given input could differ from the real command to be suggested (if >1/3 of course)
SIMILARITY_SUGGEST_FACTOR = 2 / 3


def load_available_handles() -> set:
    """
    Load all available template handles.

    :return: A set of all available handles
    """
    available_templates = load_yaml_file(f"{AVAILABLE_TEMPLATES_PATH}")
    unsplit_handles: Set[str] = set()
    all_handles: Set[str] = set()
    nested_dict_to_handle_set(available_templates, unsplit_handles)
    all_handles.update(unsplit_handles)
    split_handles(unsplit_handles, all_handles)

    return all_handles


def nested_dict_to_handle_set(available_templates, unsplitted_handles: set) -> None:
    """
    Extract the handles from loaded yml file.

    :param available_templates: The loaded yml file as a (nested) dict
    :param unsplitted_handles: The set to save the handles
    """
    if is_nested_dictionary(available_templates):
        for templ in available_templates.values():
            if not is_nested_dictionary(templ):
                unsplitted_handles.add(templ["handle"])
            else:
                nested_dict_to_handle_set(templ, unsplitted_handles)
    else:
        # a single template to append was reached
        unsplitted_handles.add(available_templates["handle"])


def split_handles(unsplitted_handles, all_handles) -> None:
    """
    Split handles into all possible combinations.

    :param unsplitted_handles: A set of unsplitted handles
    :param all_handles: All handles Cookietemple currently supports
    """
    for handle in unsplitted_handles:
        parts = handle.split("-")

        if len(parts) == 2:
            all_handles.add(parts[0])
        elif len(parts) == 3:
            all_handles.add(parts[0])
            all_handles.add(f"{parts[0]}-" + parts[1])
