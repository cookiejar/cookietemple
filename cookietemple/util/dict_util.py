from collections import MutableMapping
from contextlib import suppress


def delete_keys_from_dict(dictionary: MutableMapping, keys: list):
    """
    deletes all key instances in an arbitrarily nested dictionary inplace

    :param dictionary: dictionary of which the keys are deleted
    :param keys: list of keys to delete
    """
    for key in keys:
        with suppress(KeyError):
            del dictionary[key]
    for value in dictionary.values():
        if isinstance(value, MutableMapping):
            delete_keys_from_dict(value, keys)
