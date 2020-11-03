from collections.abc import MutableMapping
from contextlib import suppress


def delete_keys_from_dict(dictionary: MutableMapping, keys: list) -> None:
    """
    Deletes all key instances in an arbitrarily nested dictionary inplace

    :param dictionary: dictionary of which the keys are deleted
    :param keys: list of keys to delete
    """
    for key in keys:
        with suppress(KeyError):
            del dictionary[key]
    for value in dictionary.values():
        if isinstance(value, MutableMapping):
            delete_keys_from_dict(value, keys)


def is_nested_dictionary(dictionary: dict) -> bool:
    """
    Determines whether a dictionary is nested or not

    :param dictionary: dictionary to examine
    :return: True if dictionary is nested, false otherwise
    """
    return any(isinstance(_, dict) for _ in dictionary.values())
