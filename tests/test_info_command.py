import pytest
from cookietemple.info.info import show_info
from cookietemple.info.levensthein_dist import (levensthein_dist, most_similar_command, AVAILABLE_HANDLES)

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
    return ['cli-python', 'cli-java', 'cli-kotlin', 'web-python', 'gui-python', 'gui-java', 'web-python_website',
            'web-python-rest']


@pytest.fixture()
def get_commands_with_similar_command_cli():
    return ['clo', 'clk', 'vli', 'xli', 'cl i']


@pytest.fixture()
def get_commands_with_similar_command_gui():
    return ['guo', 'gzi', 'hui', 'fui', 'gui']


@pytest.fixture()
def get_commands_with_similar_command_web():
    return ['wsb', 'wrb', 'eeb', 'wev', 'wen', 'weg']


@pytest.fixture()
def get_commands_with_similar_command_cli_with_language():
    return ['cli-pyton', 'clipython', 'cli pyton', 'clipyton', 'clupython']


@pytest.fixture()
def get_commands_with_similar_command_gui_with_language():
    return ['gui-pyton', 'guipyton', 'gui python', 'gui pyton', 'guipyton']


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


@pytest.mark.skip(reason="")
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
    assert (levensthein_dist('horse', 'ros') == 3 and levensthein_dist('', 'hello') == 5 and
            levensthein_dist('lululul', '') == 7 and levensthein_dist('intention', 'execution') == 5)


def test_most_similar_command_cli(get_commands_with_similar_command_cli) -> None:
    """
    This test tests our most similar command suggestion if the user enters a domain/subdomain unknown
    to cookietemple.
    It should suggest a similar command within a certain range of similarity (e.g clo -> cli;
    but not cko -> cli).

    The output is a (possible empty) list with similar commands (thus, having the same levensthein distance to
    what the user entered).
    """
    for com in get_commands_with_similar_command_cli:
        assert most_similar_command(com, AVAILABLE_HANDLES) == ['cli']


def test_most_similar_command_web(get_commands_with_similar_command_web) -> None:
    """
    This test the most similar command for web (without any subdomain)
    """
    for com in get_commands_with_similar_command_web:
        assert most_similar_command(com, AVAILABLE_HANDLES) == ['web']


def test_most_similar_command_gui(get_commands_with_similar_command_gui) -> None:
    """
    This test the most similar command for gui (without any subdomain)
    """
    for com in get_commands_with_similar_command_gui:
        assert most_similar_command(com, AVAILABLE_HANDLES) == ['gui']


def test_most_similar_command_cli_with_language(get_commands_with_similar_command_cli_with_language) -> None:
    """
    This test the most similar command for cli with language specified
    """
    for com in get_commands_with_similar_command_cli_with_language:
        assert most_similar_command(com, AVAILABLE_HANDLES) == ['cli-python']


def test_most_similar_command_gui_with_language(get_commands_with_similar_command_gui_with_language) -> None:
    """
    This test the most similar command for gui with language specified
    """
    for com in get_commands_with_similar_command_gui_with_language:
        assert most_similar_command(com, AVAILABLE_HANDLES) == ['gui-python']
