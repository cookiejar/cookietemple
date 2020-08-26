import os
import sys
import pytest

from cookietemple.config.config import ConfigCommand
from cookietemple.create.template_creator import TemplateCreator
from cookietemple.create.create import choose_domain
from cookietemple.create.domains.cli_creator import CliCreator
import cookietemple.create.template_creator


@pytest.fixture
def get_template_cli_creators():
    """
    Return a cli creator (can be used for adding more and returning a list then)
    """
    return CliCreator


def test_if_repo_already_exists_no_overwrite(mocker, tmp_path) -> None:
    """
    Ensure that if a project with the same name already exists the user can decide to overwrite or not.
    If no, template creation will be canceled an nothing changes.

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"\n\nHomer\nsimpson@gmail.com\nhomergithub\nnExplodingSpringfield\ndescription\n1.0.0\n\n\n\nn"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    os.write(w, b"n")
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(cookietemple.create.template_creator, 'is_git_repo', autospec=True)
    cookietemple.create.template_creator.is_git_repo.return_value = False
    mocker.patch.object(TemplateCreator, 'readthedocs_slug_already_exists', autospec=True)
    TemplateCreator.readthedocs_slug_already_exists.return_value = False
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'

    with pytest.raises(SystemExit):
        choose_domain('')


def test_general_prompts_all_input_valid(tmp_path, mocker) -> None:
    """
    Ensure that valid inputs for general prompts for all template are processed properly.

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer\nsimpson@gmail.com\nhomergithub\nn"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    os.write(w, b"ExplodingSpringfield\nSpringfieldDescription\n1.0.0\n\n")

    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(TemplateCreator, 'readthedocs_slug_already_exists', autospec=True)
    TemplateCreator.readthedocs_slug_already_exists.return_value = False
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'

    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration(dot_cookietemple={})
    assert (test_creator.cli_struct.full_name == 'Homer' and test_creator.cli_struct.email == 'simpson@gmail.com' and
            test_creator.cli_struct.github_username == 'homergithub' and test_creator.cli_struct.project_name == 'ExplodingSpringfield' and
            test_creator.cli_struct.project_short_description == 'SpringfieldDescription' and test_creator.cli_struct.version == '1.0.0' and
            test_creator.cli_struct.license == 'MIT' and test_creator.cli_struct.project_slug == 'ExplodingSpringfield' and
            test_creator.cli_struct.project_slug_no_hyphen == 'ExplodingSpringfield')


def test_general_prompts_with_hyphen_slug(mocker, tmp_path) -> None:
    """
    Ensure that entering a project name containg a hyphen will lead to correct project_name and project_slug set

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer\nsimpson@gmail.com\nhomergithub\nn"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    os.write(w, b"Exploding-Springfield\nSpringfieldDescription\n1.0.0\n\n")

    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(TemplateCreator, 'readthedocs_slug_already_exists', autospec=True)
    TemplateCreator.readthedocs_slug_already_exists.return_value = False
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'

    test_creator = CliCreator()
    test_creator.prompt_general_template_configuration(dot_cookietemple={})
    assert (test_creator.cli_struct.full_name == 'Homer' and test_creator.cli_struct.email == 'simpson@gmail.com' and
            test_creator.cli_struct.github_username == 'homergithub' and test_creator.cli_struct.project_name == 'Exploding-Springfield' and
            test_creator.cli_struct.project_short_description == 'SpringfieldDescription' and test_creator.cli_struct.version == '1.0.0' and
            test_creator.cli_struct.license == 'MIT' and test_creator.cli_struct.project_slug == 'Exploding-Springfield' and
            test_creator.cli_struct.project_slug_no_hyphen == 'Exploding_Springfield')
