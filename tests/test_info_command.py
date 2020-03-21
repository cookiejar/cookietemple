import pytest
from cookietemple.info.info import show_info
from cookietemple.info.levensthein_dist import (levensthein_dist, most_similar_command)

"""
This test class is for testing the info subcommand:

Syntax: cookietemple info [domain](-)([subdomain])

A non existing or not understood domain/subdomain should result in a KeyError
"""


@pytest.fixture()
def get_invalid_handles():
    """
    Defines invalids handlers
    """
    return ['pythOn', '1234', 'Aw3s0m3', 'javaa', 'python--web', 'java-web', 'web-kotlin']


@pytest.fixture()
def get_valid_handles_domain_only():
    return ['cli', 'web', 'gui']


@pytest.fixture()
def get_valid_handles_domain_subdomain():
    return ['cli-python', 'cli-java', 'cli-kotlin', 'web-python', 'gui-python', 'gui-java', 'web-python_website', 'web-python-rest']


@pytest.mark.skip(reason="Idk how to test this: We have to use mocking in some way")
def test_empty_info_handle():
    show_info('')


def test_non_existing_handle(get_invalid_handles, capfd) -> None:
    """
    Ensure that a non-valid/existing handle will trigger an error message
    """

    for invalid in get_invalid_handles:
        with pytest.raises(SystemExit):
            show_info(invalid)
            out, err = capfd.readouterr()
            assert out == 'Handle does not exist. Please enter a valid handle. Use ' + 'cookietemple list' + ' to display all template handles.'


def test_valid_handles_domain_only(get_valid_handles_domain_only, capfd) -> None:
    """
    Ensure that valid handles will be displayed properly by the info command.
    """

    for valid_domain in get_valid_handles_domain_only:
        show_info(valid_domain)
        out, err = capfd.readouterr()

        if valid_domain == 'cli':
            assert out.startswith('\n\nTemplate info for cli')
        elif valid_domain == 'web':
            assert out.startswith('\n\nTemplate info for web')
        elif valid_domain == 'gui':
            assert out.startswith('\n\nTemplate info for gui')


@pytest.mark.xfail
def test_valid_handles_domain_and_subdomain(get_valid_handles_domain_subdomain, capfd) -> None:
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


def test_levensthein_dist() -> None:
    """
    This test tests our implemented levensthein distance function for measuring string similarity.
    """
    assert (levensthein_dist("horse", "ros") == 3 and levensthein_dist("", "hello") == 5 and
            levensthein_dist("lululul", "") == 7 and levensthein_dist("intention", "execution") == 5)


@pytest.mark.skip(reason="Tomorrow")
def test_most_similar_command() -> None:
    """
    TODO: TIRED WILL DO THIS TOMORROW BECAUSE WE NEED GOOD TESTCASES
    :return:
    """
    most_similar_command()
