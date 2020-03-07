import pytest
from cookietemple.info.info import (show_info, non_existing_handle)

"""
    This test class is for testing the info subcommand:

    Syntax: cookietemple info [domain]([subdomain])

    A non existing or not understood domain/subdomain should result in a KeyError
"""


# define some invalid handles
@pytest.fixture()
def get_invalid_handles():
    return ['pythOn', '1234', 'Aw3s0m3', 'javaa', 'python--web', 'java-web', 'web-kotlin']


# use built-in fixture for capture sys.stdout
def test_info_handle_is_empty(capfd):
    show_info("")
    out, err = capfd.readouterr()
    assert out == 'Please enter the possibly incomplete template handle. Examples: \'cli-python\' or \'cli\''


def test_non_existing_handle(get_invalid_handles, capfd):
    for invalid in get_invalid_handles:
        with pytest.raises(SystemExit):
            show_info(invalid)
            out, err = capfd.readouterr()
            assert out == 'Handle does not exist. Please enter a valid handle. Use ' + 'cookietemple list' + ' to display all template handles.'
