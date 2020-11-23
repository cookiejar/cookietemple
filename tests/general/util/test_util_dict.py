import pytest  # type: ignore

from cookietemple.util.dict_util import (delete_keys_from_dict, is_nested_dictionary)


@pytest.fixture()
def some_nested_dictionaries():
    """
    Some nested dicts.
    """
    return [{1: 0, 2: {1: 0, 0: 0}}, {1: {1: {1: 0}}}, {1: 0, 0: 1, 2: 0, 3: 3, 5: {1: {1: {1: 0}}}, 4: 0}]


@pytest.fixture()
def some_unnested_dictionaries():
    """
    Some unnested dicts.
    """
    return [{}, {1: 0, 0: 0, 2: 1}, {"a": 0, "b": 0, "c": 1}, {1: 0, 0: 0, 2: [0, 2, 3, 4]}]


@pytest.fixture
def delete_those_keys():
    """
    Return keys that should be deleted in a dict.
    """
    return [0, "a", 1, 4, 3, 2]


def test_is_nested_dictionary(some_nested_dictionaries, some_unnested_dictionaries):
    """
    Return whether a dictionary is nested or not.
    """
    for dictn in some_nested_dictionaries:
        assert is_nested_dictionary(dictn)
    for dictn in some_unnested_dictionaries:
        assert not is_nested_dictionary(dictn)


def test_delete_keys_from_dict(some_nested_dictionaries, some_unnested_dictionaries, delete_those_keys):
    """
    Delete keys from a dict and ensure they are deleted.
    """
    for key in delete_those_keys:
        for dictn in some_nested_dictionaries:
            delete_keys_from_dict(dictn, [key])
            assert key not in dictn
        for dictn in some_unnested_dictionaries:
            delete_keys_from_dict(dictn, [key])
            assert key not in dictn
