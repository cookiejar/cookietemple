import os
import pytest
from io import StringIO

from cookietemple.create.create import choose_domain
from cookietemple.create.domains.cli_creator import CliCreator


@pytest.fixture
def get_template_cli_creators():
    """
    Return a cli creator (can be used for adding more and returning a list then)
    """
    return CliCreator


def test_if_repo_already_exists_no_overwrite(mocker, monkeypatch, capfd) -> None:
    """
    Ensure that if a project with the same name already exists the user can decide to overwrite or not.
    If no, template creation will be canceled an nothing changes.
    """
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    prompt = StringIO('cli\npython\ntestname\ntestmail\nblablakdsad\ndesc\n0.1.1\nMIT\nmyGitHubName\nClick\npytest\nN')
    monkeypatch.setattr('sys.stdin', prompt)

    with pytest.raises(SystemExit):
        choose_domain('')
        out, err = capfd.readouterr()
        assert out.strip() == 'Aborted! Canceled template creation!'


def test_general_prompts_all_input_valid(monkeypatch) -> None:
    """
    Ensure that valid inputs for general prompts for all template are processed properly.
    """

    prompts = StringIO('MyFullName\nMyEmail\nMyProjectName\nMyDesc\n0.1.0\nMIT\nmygithubusername')
    monkeypatch.setattr('sys.stdin', prompts)
    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration()
    test_creator.cli_struct.github_username = 'mygithubusername'
    assert (test_creator.cli_struct.full_name == 'MyFullName' and test_creator.cli_struct.email == 'MyEmail' and
            test_creator.cli_struct.project_slug == 'MyProjectName' and test_creator.cli_struct.project_short_description == 'MyDesc' and
            test_creator.cli_struct.version == '0.1.0' and test_creator.cli_struct.license == 'MIT' and
            test_creator.cli_struct.github_username == 'mygithubusername')


def test_general_prompts_with_license_invalid_choice(monkeypatch, capfd) -> None:
    """
    Ensure that entering an invalid license will trigger an error message.
    """
    prompts = StringIO('MyFullName\nMyEmail\nMyProjectName\nMyDesc\n0.1.0\nÄMAITI\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)

    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration()
    out, err = capfd.readouterr()
    assert 'Error: invalid choice: ÄMAITI.' in out.strip()
