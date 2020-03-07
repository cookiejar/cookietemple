import pytest
import pytest_mock
from unittest.mock import patch, mock_open
from pathlib import Path
from cookietemple.create.create_config import (delete_dir_tree, TEMPLATE_STRUCT, prompt_general_template_configuration,
                                               create_dot_cookietemple)
from io import StringIO


# init a test TEMPLATE_STRUCT dict with valid values
@pytest.fixture()
def init_template_struct():
    TEMPLATE_STRUCT['fullname'] = 'MyFullName'
    TEMPLATE_STRUCT['email'] = 'MyEmail'
    TEMPLATE_STRUCT['github_username'] = 'MyGitName'
    TEMPLATE_STRUCT['project_name'] = 'ProjectName'
    TEMPLATE_STRUCT['project_slug'] = 'MySlug'
    TEMPLATE_STRUCT['project_short_description'] = 'MyDesc'
    TEMPLATE_STRUCT['version'] = 'MyVersion'
    TEMPLATE_STRUCT['license'] = 'MIT'
    TEMPLATE_STRUCT['template_version'] = 'MyTemplateVersion'
    TEMPLATE_STRUCT['template_handle'] = 'cli-python'  # CAVE!!! handler

    return TEMPLATE_STRUCT


# mock click prompt input
def test_general_prompts_all_input_valid(monkeypatch):
    prompts = StringIO('MyFullName\nMyEmail\nMyGitName\nMyProjectName\nMySlug\nMyDesc\nMyVersion\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    prompt_general_template_configuration()
    assert (TEMPLATE_STRUCT['full_name'] == 'MyFullName' and TEMPLATE_STRUCT['email'] == 'MyEmail'
            and TEMPLATE_STRUCT['github_username'] == 'MyGitName' and TEMPLATE_STRUCT['project_name'] == 'MyProjectName'
            and TEMPLATE_STRUCT['project_slug'] == 'MySlug' and TEMPLATE_STRUCT['project_short_description'] == 'MyDesc'
            and TEMPLATE_STRUCT['version'] == 'MyVersion' and TEMPLATE_STRUCT['license'] == 'MIT')


# mock click prompt input
def test_general_prompts_with_license_invalid_choice(monkeypatch, capfd):
    prompts = StringIO('MyFullName\nMyEmail\nMyGitName\nMyProjectName\nMySlug\nMyDesc\nMyVersion\nIMALICENSE\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    prompt_general_template_configuration()
    out, err = capfd.readouterr()
    assert 'Error: invalid choice: IMALICENSE.' in out.strip()


def test_create_dot_cookietemple_file():
    open_mock = mock_open()
    with patch("cookietemple.create.create_config.open", open_mock, create=True):
        create_dot_cookietemple(TEMPLATE_STRUCT, "MyOtherVersion", "MyOtherHandle")

    open_mock.assert_called_with(f'{TEMPLATE_STRUCT["project_slug"]}/.cookietemple', "w")


def test_del_dir_tree(tmp_path):
    dir = tmp_path / "testIT"
    a = dir / "a"
    b = dir / "b"
    dir.mkdir()
    a.mkdir()
    b.mkdir()
    p = dir / "hello.txt"
    p.write_text("HelloTESTFILE")
    af = a / "MyATestFile"
    bf = b / "MyBTestFile"

    delete_dir_tree(dir)
    assert len(list(tmp_path.iterdir())) == 0


# some testing setup, will be deleted later (from pytest doc)
def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'

    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
