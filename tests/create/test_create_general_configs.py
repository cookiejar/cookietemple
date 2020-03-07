import pytest
import pytest_mock
from pathlib import Path
from cookietemple.create.create_config import (delete_dir_tree, TEMPLATE_STRUCT, prompt_general_template_configuration)
from io import StringIO


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
def test_general_prompts_with_license_invalid_choice(monkeypatch,capfd):
    prompts = StringIO('MyFullName\nMyEmail\nMyGitName\nMyProjectName\nMySlug\nMyDesc\nMyVersion\nIMALICENSE\nMIT')
    monkeypatch.setattr('sys.stdin', prompts)
    prompt_general_template_configuration()
    out, err = capfd.readouterr()
    assert 'Error: invalid choice: IMALICENSE.' in out.strip()


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
