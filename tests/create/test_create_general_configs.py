import os
import tempfile
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.create.create_templates import (create_dot_cookietemple, create_common_files)
from cookietemple.create.create_config import (TEMPLATE_STRUCT, prompt_general_template_configuration)
from io import StringIO


# init a test TEMPLATE_STRUCT dict with valid values
@pytest.fixture()
def init_template_struct() -> set:
    TEMPLATE_STRUCT['fullname'] = 'MyFullName'
    TEMPLATE_STRUCT['email'] = 'MyEmail'
    TEMPLATE_STRUCT['project_name'] = 'ProjectName'
    TEMPLATE_STRUCT['project_short_description'] = 'MyDesc'
    TEMPLATE_STRUCT['version'] = '0.1.0'
    TEMPLATE_STRUCT['license'] = 'MIT'
    TEMPLATE_STRUCT['template_version'] = '0.1.1'
    TEMPLATE_STRUCT['template_handle'] = 'cli-python'  # CAVE!!! handler
    TEMPLATE_STRUCT['language'] = 'python'

    return TEMPLATE_STRUCT


def test_general_prompts_all_input_valid(monkeypatch) -> None:
    """
    Ensure that valid inputs for the genereal prompts for all template are processed properly.
    """
    prompts = StringIO('MyFullName\nMyEmail\nMyProjectName\nMyDesc\n0.1.0\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    prompt_general_template_configuration()
    assert (TEMPLATE_STRUCT['full_name'] == 'MyFullName' and TEMPLATE_STRUCT['email'] == 'MyEmail'
            and TEMPLATE_STRUCT['project_name'] == 'MyProjectName'
            and TEMPLATE_STRUCT['project_short_description'] == 'MyDesc'
            and TEMPLATE_STRUCT['version'] == '0.1.0' and TEMPLATE_STRUCT['license'] == 'MIT')


def test_general_prompts_with_license_invalid_choice(monkeypatch, capfd) -> None:
    """
    Ensure that entering an invalid license will trigger an error message.
    """
    prompts = StringIO('MyFullName\nMyEmail\nMyProjectName\nMyDesc\n0.1.0\nIMALICENSE\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    prompt_general_template_configuration()
    out, err = capfd.readouterr()
    assert 'Error: invalid choice: IMALICENSE.' in out.strip()


def test_create_dot_cookietemple_file() -> None:
    """
    Ensure that the .cookietemple.yml file is created using the right arguments.
    """
    open_mock = mock_open()
    with patch('cookietemple.create.create_templates.open', open_mock, create=True):
        create_dot_cookietemple(TEMPLATE_STRUCT, 'MyOtherVersion', 'MyOtherHandle')

    open_mock.assert_called_with(f'{TEMPLATE_STRUCT["project_name"]}/.cookietemple.yml', 'w')


def test_del_dir_tree(tmp_path) -> None:
    """
    Ensure that this function deletes a random directory with subdirectories and files
    """
    dir = tmp_path / 'testIT'
    a = dir / 'a'
    b = dir / 'b'
    dir.mkdir()
    a.mkdir()
    b.mkdir()
    p = dir / 'hello.txt'
    p.write_text('HelloTESTFILE')
    af = a / 'MyATestFile'  # noqa: F841
    bf = b / 'MyBTestFile'  # noqa: F841

    delete_dir_tree(dir)
    assert len(list(tmp_path.iterdir())) == 0


@pytest.mark.skip(reason='Fix this test later on')
def test_create_common_files(mocker, tmp_path) -> None:
    """
    This test should test a isolated common files creation function.
    """
    # mock current working directory for common_files tests TODO:FIX TEST

    mocker.patch.object(Path, 'cwd', autospec=True)
    mocker.patch.object(os, 'getcwd', autospec=True)
    mocker.patch.object(tempfile, 'mkdtemp', autospec=True)
    Path.cwd.return_value = str(tmp_path)
    os.getcwd.return_value = str(tmp_path)
    tempfile.mkdtemp.return_value = str(tmp_path)

    TEMPLATE_STRUCT['fullname'] = 'MyFullName'
    TEMPLATE_STRUCT['email'] = 'MyEmail'
    TEMPLATE_STRUCT['github_username'] = 'MyGitName'
    TEMPLATE_STRUCT['project_name'] = 'ProjectName'
    TEMPLATE_STRUCT['project_slug'] = 'MySlug'
    TEMPLATE_STRUCT['project_short_description'] = 'MyDesc'
    TEMPLATE_STRUCT['version'] = '0.1.0'
    TEMPLATE_STRUCT['license'] = 'MIT'
    TEMPLATE_STRUCT['template_version'] = '0.1.1'
    TEMPLATE_STRUCT['template_handle'] = 'cli-python'  # CAVE!!! handler
    TEMPLATE_STRUCT['language'] = 'python'

    create_common_files()

    assert 1 == 1  # PLACEHOLDER
