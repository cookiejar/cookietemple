import pytest
import click
from pytest_mock import mocker
from cookietemple.info.info import (show_info, non_existing_handle)

"""
    This test class is for testing the info subcommand:

    Syntax: cookietemple info [domain](-)([subdomain])

    A non existing or not understood domain/subdomain should result in a KeyError
"""


# define some invalid handles
@pytest.fixture()
def get_invalid_handles():
    return ['pythOn', '1234', 'Aw3s0m3', 'javaa', 'python--web', 'java-web', 'web-kotlin']


@pytest.fixture()
def get_valid_handles_domain_only():
    return ['cli', 'web', 'gui']

@pytest.fixture()
def get_valid_handles_domain_subdomain():
    return ['cli-python', 'cli-java', 'cli-kotlin', 'web-python', 'gui-python', 'gui-java', 'web-python_website',
            'web-python-rest']


@pytest.mark.skip(reason="Idk how to test this: We have to use mocking in some way")
def test_empty_info_handle():
    show_info('')  # how to test interactive functions (click.prompt)?


def test_non_existing_handle(get_invalid_handles, capfd):
    for invalid in get_invalid_handles:
        with pytest.raises(SystemExit):
            show_info(invalid)
            out, err = capfd.readouterr()
            assert out == 'Handle does not exist. Please enter a valid handle. Use ' + 'cookietemple list' + ' to display all template handles.'


def test_valid_handles_domain_only(get_valid_handles_domain_only, capfd):
    for valid_domain in get_valid_handles_domain_only:
        show_info(valid_domain)
        out, err = capfd.readouterr()

        if valid_domain is 'cli':
            assert out.startswith('\nTemplate info for cli\n\npython:\n  handle: cli-python\n  version: 0.0.1\n')
        elif valid_domain is 'web':
            assert out.startswith('\nTemplate info for web\n\nwebsite:\n  python:\n    handle: web-website-python\n    version: 0.0.1\n')
        elif valid_domain is 'gui':
            assert out.startswith('\nTemplate info for gui\n\npython:\n  handle: gui-python\n')


def test_valid_handles_domain_and_subdomain(get_valid_handles_domain_subdomain, capfd):
    for valid_domain_subdomain in get_valid_handles_domain_subdomain:
        show_info(valid_domain_subdomain)
        out, err = capfd.readouterr()

        switcher = {
            'cli-python': '\nTemplate info for cli-python\n\nhandle: cli-python\n',
            'gui-python': '\nTemplate info for gui-python\n\nhandle: gui-python\n',
            'cli-java': '\nTemplate info for cli-java\n\nhandle: cli-java\n',
            'gui-java': '\nTemplate info for gui-java\n\nhandle: gui-java\n',
            'cli-kotlin': '\nTemplate info for cli-kotlin\n\nhandle: cli-kotlin\n',
            'web-python': '\nTemplate info for web\n\nwebsite:\n  python:\n',
            'web-python_website': '\nSOME TEXT!!',
            'web-python-rest': '\nSOME TEXTAGAIN!!'
            }

        assert out.startswith(switcher.get(valid_domain_subdomain))
