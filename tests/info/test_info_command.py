from typing import Dict

import pytest
from click.testing import CliRunner

from cookietemple.__main__ import info
from cookietemple.common.levensthein_dist import most_similar_command
from cookietemple.info.info import TemplateInfo

"""
This test class is for testing the info subcommand:

Syntax: cookietemple info [domain](-)([subdomain])

A non existing or not understood domain/subdomain as well as an empty argument should result in an Error.
"""


@pytest.fixture()
def get_invalid_handles():
    """
    Defines invalids handlers
    """
    return ["1234", "Aw3s0m3", "python--web", "javsadsaaafafsfsf", "somelongnonexisitinghandle", "-"]


@pytest.fixture()
def get_valid_handles_domain_only():
    """
    Define valid domain handles
    """
    return ["cli", "web", "gui", "pub"]


@pytest.fixture()
def get_valid_handles_domain_subdomain():
    """
    Define valid handles with domain AND subdomain
    """
    return ["cli-python", "cli-java", "gui-java", "web-website", "web-website-python", "pub-thesis", "pub-thesis-latex"]


@pytest.fixture()
def get_commands_with_similar_command_cli():
    """
    Define similar arguments to 'cli' that should result in suggestion of the most similar arg 'cli'
    """
    return ["clo", "clk", "vli", "xli", "cl i", "clu", "CLU", "ClU", "cLI", "Cli", "cLI"]


@pytest.fixture()
def get_commands_with_similar_command_gui():
    """
    Define similar arguments to 'gui' that should result in suggestion of the most similar arg 'gui'
    """
    return ["guo", "gzi", "hui", "fui", "gui", "GUI", "gUi", "Gui", "gUI"]


@pytest.fixture()
def get_commands_with_similar_command_web():
    """
    Define similar arguments to 'web' that should result in suggestion of the most similar arg 'web'
    """
    return ["wsb", "wrb", "eeb", "wev", "wen", "weg", "WEB", "Web", "wEB"]


@pytest.fixture()
def get_commands_with_similar_command_pub():
    """
    Define similar arguments to 'pub' that should result in suggestion of the most similar arg 'pub'
    """
    return ["pib", "PUB", "Pub", "pUB", "pup", "pub-", "pun", "puv"]


@pytest.fixture()
def get_commands_with_similar_command_cli_with_language():
    """
    Define handles of cli domain with language
    """
    return [
        "cli-pyton",
        "clipython",
        "cli python",
        "clipyton",
        "clupython",
        "CLI-PYTHON",
        "cLI_PYTHON",
        "cli-Java",
        "cLI_JAVA",
        "clijava",
        "cli-javaa",
    ]


@pytest.fixture()
def get_commands_with_similar_command_gui_with_language():
    """
    Define handles of cli domain with language
    """
    return ["gui-jav", "guijaa", "guijava", "guijav", "GUI-JAVA", "gUI_JAVA"]


@pytest.fixture()
def get_commands_with_similar_command_web_with_subdomain_and_language():
    """
    Define handles of web domain with subdomain and language
    """
    return [
        "web-websit",
        "WEB_WEBSITE",
        "web-ebsite",
        "wenwebsite",
        "webwebsite",
        "wEB_WEBSITE",
        "web-websit-python",
        "WEB_WEBSITE_PYTHON",
        "web-ebsitepython",
        "wenwebsitepython",
        "webwebsite-python",
        "wEB_WEBSITE_PYTHON",
        "WEBWEBSITEPYTHON",
    ]


@pytest.fixture()
def get_commands_with_similar_command_pub_with_subdomain_and_language():
    """
    Define handles of pub domain with subdomain and language
    """
    return [
        "pub-tesis",
        "PUB_THESIS",
        "pubthesis",
        "pubthese",
        "pub-these",
        "pUB_THESIS",
        "pub-these-latex",
        "pUB_THESIS_LATEX",
        "pub-thesislatex",
        "pubthesislatex",
        "pub-thesislatex",
        "PUB_THESIS_LATEX",
        "PUBTHESISLATEX",
    ]


@pytest.fixture()
def get_all_valid_handles_as_set(get_valid_handles_domain_subdomain, get_valid_handles_domain_only):
    """
    Return all possible available handles
    """
    return set(get_valid_handles_domain_subdomain).union(set(get_valid_handles_domain_only))


@pytest.fixture()
def get_valid_languages():
    """
    Define handles of all available languages
    """
    return ["python", "Python", "java", "Java", "latex", "Latex"]


# TEST SECTION ========================================================


def test_empty_handle_throws_error():
    """
    Ensure that info command requires a non-empty argument
    """
    runner = CliRunner()
    result = runner.invoke(info, [""])

    assert result.exit_code == 1


def test_non_existing_handle(get_invalid_handles, capfd) -> None:
    """
    Ensure that a non-valid/existing handle will trigger an error message
    """
    runner = CliRunner()
    for invalid in get_invalid_handles:
        result = runner.invoke(info, [invalid])
        assert result.exit_code == 0


@pytest.mark.skip(reason="Check, how to test output of a rich Table")
def test_valid_handles_domain_only(get_valid_handles_domain_only, capfd) -> None:
    """
    Ensure that valid handles will be displayed properly by the info command.
    """
    switcher = {
        "cli": ("cli-python", "cli-java"),
        "web": "web-website-python",
        "gui": "gui-java",
        "pub": "pub-thesis-latex",
    }

    for valid_domain in get_valid_handles_domain_only:
        template_info = TemplateInfo()
        template_info.show_info(valid_domain)
        out, err = capfd.readouterr()

        for handle in switcher[valid_domain]:
            assert handle in out


def test_valid_languages_only(get_valid_languages) -> None:
    """
    Ensure that valid language handles will be displayed properly by the info command (and only those).
    """
    switcher = {
        ("python", "Python"): ("java", "latex"),
        ("java", "Java"): ("python", "latex"),
        ("latex", "Latex"): ("java", "python"),
    }

    runner = CliRunner()
    for valid_language in get_valid_languages:
        result = runner.invoke(info, [valid_language])
        assert (
            result.exit_code == 0
            and valid_language.lower() in result.output
            and not any(lan in result.output for lan in [v for k, v in switcher.items() if valid_language in k][0])
        )


@pytest.mark.skip(reason="Check, how to test output of a rich Table")
def test_valid_handles_domain_and_subdomain(get_valid_handles_domain_subdomain, capfd) -> None:
    """
    Test if a valid combination of domain and subdomain produces correct output
    """
    for valid_domain_subdomain in get_valid_handles_domain_subdomain:
        template_info = TemplateInfo()
        template_info.show_info(valid_domain_subdomain)
        out, err = capfd.readouterr()

        # first entry of value list are expected handles present in output second are the ones that should not be in output
        switcher: Dict[str, list] = {
            "cli-python": [["cli-python"], "cli-java"],
            "cli-java": [["cli-java"], "cli-python"],
            "gui-java": [["gui-java"]],
            "web-website": [["web-website"], [""]],
            "web-website-python": [["web-website-python"], [""]],
            "pub-thesis": [["pub-thesis"], [""]],
            "pub-thesis-latex": [["pub-thesis-latex"], [""]],
        }

        for exp_handle in switcher[valid_domain_subdomain][0]:
            assert exp_handle in out and not any(
                not_exp_handle in out for not_exp_handle in switcher[valid_domain_subdomain][1] if not_exp_handle
            )


def test_most_similar_command_cli(get_commands_with_similar_command_cli, get_all_valid_handles_as_set) -> None:
    """
    Test our most similar command suggestion (here: cli) if the user enters a domain/subdomain unknown to cookietemple.
    It should suggest a similar command within a certain range of similarity (e.g clo -> cli but not asd -> cli).
    """
    for com in get_commands_with_similar_command_cli:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert test_tuple[0] == ["cli"] and test_tuple[1] == "use"


def test_most_similar_command_web(get_commands_with_similar_command_web, get_all_valid_handles_as_set) -> None:
    """
    Test the most similar command for web (without any subdomain)
    """
    for com in get_commands_with_similar_command_web:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert test_tuple[0] == ["web"] and test_tuple[1] == "use"


def test_most_similar_command_gui(get_commands_with_similar_command_gui, get_all_valid_handles_as_set) -> None:
    """
    Test the most similar command for web (without any subdomain)
    """
    for com in get_commands_with_similar_command_gui:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert test_tuple[0] == ["gui"] and test_tuple[1] == "use"


def test_most_similar_command_pub(get_commands_with_similar_command_pub, get_all_valid_handles_as_set) -> None:
    """
    Test the most similar command for web (without any subdomain)
    """
    for com in get_commands_with_similar_command_pub:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert test_tuple[0] == ["pub"] and test_tuple[1] == "use"


def test_most_similar_command_cli_with_language(
    get_commands_with_similar_command_cli_with_language, get_all_valid_handles_as_set
) -> None:
    """
    Test the most similar command for cli with language specified.
    All is needed in the rare case if there are multiple similar handles.
    """
    for com in get_commands_with_similar_command_cli_with_language:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert all(handle in {"cli-python", "cli-java"} for handle in test_tuple[0])


def test_most_similar_command_gui_with_language(
    get_commands_with_similar_command_gui_with_language, get_all_valid_handles_as_set
) -> None:
    """
    Test the most similar command for cli with language specified.
    All is needed in the rare case if there are multiple similar handles.
    """
    for com in get_commands_with_similar_command_gui_with_language:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert all(handle in {"gui-java"} for handle in test_tuple[0])


def test_most_similar_command_web_with_subdomain_and_language(
    get_commands_with_similar_command_web_with_subdomain_and_language, get_all_valid_handles_as_set
) -> None:
    """
    This test the most similar command for cli with language specified.
    All is needed in the rare case if there are multiple similar handles.
    """
    for com in get_commands_with_similar_command_web_with_subdomain_and_language:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert all(handle in {"web-website", "web-website-python"} for handle in test_tuple[0])


def test_most_similar_command_pub_with_subdomain_and_language(
    get_commands_with_similar_command_pub_with_subdomain_and_language, get_all_valid_handles_as_set
) -> None:
    """
    This test the most similar command for cli with language specified.
    All is needed in the rare case if there are multiple similar handles.
    """
    for com in get_commands_with_similar_command_pub_with_subdomain_and_language:
        test_tuple = most_similar_command(com.lower(), get_all_valid_handles_as_set)
        assert all(handle in {"pub-thesis", "pub-thesis-latex"} for handle in test_tuple[0])
