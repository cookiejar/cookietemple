import os
from pathlib import Path
import pytest
from io import StringIO

from cookietemple.config_command.config import ConfigCommand
from cookietemple.create.create import choose_domain
from cookietemple.create.domains.cli_creator import CliCreator
import cookietemple.create.template_creator


@pytest.fixture
def get_template_cli_creators():
    """
    Return a cli creator (can be used for adding more and returning a list then)
    """
    return CliCreator


def test_if_repo_already_exists_no_overwrite(mocker, monkeypatch, capfd, tmp_path) -> None:
    """
    Ensure that if a project with the same name already exists the user can decide to overwrite or not.
    If no, template creation will be canceled an nothing changes.
    """
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(Path, 'cwd', autospec=True)
    Path.cwd.return_value = tmp_path
    mocker.patch.object(cookietemple.create.template_creator, 'is_git_repo', autospec=True)
    cookietemple.create.template_creator.is_git_repo.return_value = False
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'

    prompt = StringIO('cli\npython\nhomer\nhomer@hotmail.com\nhomergithub\nn\nprojectname\ndesc\n0.1.1\nMIT\nClick\npytest\nN')
    monkeypatch.setattr('sys.stdin', prompt)

    with pytest.raises(SystemExit):
        choose_domain('')
        out, err = capfd.readouterr()
        assert out.strip() == 'Aborted! Canceled template creation!'


def test_general_prompts_all_input_valid(monkeypatch, tmp_path, mocker) -> None:
    """
    Ensure that valid inputs for general prompts for all template are processed properly.
    """
    mocker.patch.object(Path, 'cwd', autospec=True)
    Path.cwd.return_value = tmp_path
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
    prompts = StringIO('Homer\nhomer.simpson@hotmail.com\nhomergithub\nn\nMyProjectName\nMyDesc\n0.1.0\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration()
    assert (test_creator.cli_struct.full_name == 'Homer' and test_creator.cli_struct.email == 'homer.simpson@hotmail.com' and
            test_creator.cli_struct.github_username == 'homergithub' and test_creator.cli_struct.project_name == 'MyProjectName' and
            test_creator.cli_struct.project_short_description == 'MyDesc' and test_creator.cli_struct.version == '0.1.0' and
            test_creator.cli_struct.license == 'MIT')


def test_general_prompts_with_license_invalid_choice(monkeypatch, capfd, mocker, tmp_path) -> None:
    """
    Ensure that entering an invalid license will trigger an error message.
    """
    mocker.patch.object(Path, 'cwd', autospec=True)
    Path.cwd.return_value = tmp_path
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
    prompts = StringIO('\nHomer\nhomer.simpson@hotmail.com\nhomergithub\nn\nMyFullName\nMyEmail\nMyProjectName\nMyDesc\n0.1.0\nÄMAITI\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)

    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration()
    out, err = capfd.readouterr()
    assert 'Error: invalid choice: ÄMAITI.' in out.strip()
