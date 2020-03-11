import pytest
import os
import pytest_mock
from io import StringIO
from pathlib import Path
from distutils.dir_util import copy_tree


from cookietemple.create.create import choose_domain
from cookietemple.util.dir_util import delete_dir_tree


@pytest.fixture
def valid_domains():
    return ['cli', 'gui', 'web']


def docs_subdir(path):
    return [Path(f"{path}/docs/conf.py"),Path(f"{path}/docs/Makefile"),Path(f"{path}/docs/contributing.rst"),Path(f"{path}/docs/authors.rst"),
            Path(f"{path}/docs/installation.rst"),Path(f"{path}/docs/make.bat"),Path(f"{path}/docs/index.rst"),Path(f"{path}/docs/usage.rst"),
            Path(f"{path}/docs/changelog.rst"),Path(f"{path}/docs/readme.rst")]


def subdir_tests(path):
    return [Path(f"{path}/tests/__init__.py"),Path(f"{path}/tests/test_projectname.py")]


def subdir_maindir(path):
    return [Path(f"{path}/projectname/__init__.py"),Path(f"{path}/projectname/cli.py"),Path(f"{path}/projectname/projectname.py"),
            Path(f"{path}/projectname/files")]


def subdir_dependabot(path):
    return [Path(f"{path}/.dependabot/config.yml")]


def subdir_github(path):
    return [Path(f"{path}/.github/ISSUE_TEMPLATE.md")]


def posix_path_super_dir(path):
    return [Path(f"{path}/MANIFEST.in"),Path(f"{path}/.editorconfig"),Path(f"{path}/Makefile"),Path(f"{path}/README.rst"),
            Path(f"{path}/tests"),Path(f"{path}/readthedocs.yml"),Path(f"{path}/tox.ini"),Path(f"{path}/requirements_dev.txt"),
            Path(f"{path}/.travis.yml"),Path(f"{path}/.gitignore"),Path(f"{path}/projectname"),Path(f"{path}/.github"),
            Path(f"{path}/setup.py"),Path(f"{path}/.cookietemple"),Path(f"{path}/CODE_OF_CONDUCT.rst"),Path(f"{path}/docs"),
            Path(f"{path}/Dockerfile"),Path(f"{path}/requirements.txt"),Path(f"{path}/setup.cfg"),Path(f"{path}/CHANGELOG.rst"),
            Path(f"{path}/CONTRIBUTING.rst"),Path(f"{path}/LICENSE"),Path(f"{path}/AUTHORS.rst"),Path(f"{path}/.dependabot"),]


# test creation of a simple cli python template
# TODO: USE LINTING (LIKE NF CORE TOOLS) TO TEST COOKIECUTTER WITH EXTRA_CONTENT
def test_choose_domain_cli(monkeypatch,valid_domains,tmp_path):
    prompt = StringIO(f"{valid_domains[0]}\npython\nname\nmail\nprojectname\ndesc\n0.1"
                      f"\nMIT\nmyGitHubName\npypiname\nClick\npytest\nn")
    monkeypatch.setattr('sys.stdin', prompt)
    choose_domain("")
    copy_tree(f'{Path.cwd()}/projectname', str(tmp_path))
    delete_dir_tree(Path(f"{Path.cwd()}/projectname"))
    assert (sorted(list(tmp_path.iterdir())) == sorted(posix_path_super_dir(tmp_path)) and sorted(list(Path(tmp_path/"docs").iterdir())) == sorted(docs_subdir(tmp_path))
            and sorted(list(Path(tmp_path/"tests").iterdir())) == sorted(subdir_tests(tmp_path)) and
            sorted(list(Path(tmp_path/".dependabot").iterdir())) == sorted(subdir_dependabot(tmp_path)) and
            sorted(list(Path(tmp_path/".github").iterdir())) == sorted(subdir_github(tmp_path))and
            sorted(list(Path(tmp_path/"projectname").iterdir())) == sorted(subdir_maindir(tmp_path)))


# TODO: Use Linter to ensure that nothing changed (cookiecutter extra content)
def test_repo_already_exists_no_overwrite_if_false(mocker,monkeypatch,capfd,valid_domains) -> None:
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    prompt = StringIO(f"{valid_domains[0]}\npython\nname\nmail\nprojectname\ndesc\n0.1"
                      f"\nMIT\nmyGitHubName\npypiname\nClick\npytest\nN")
    monkeypatch.setattr('sys.stdin',prompt)

    with pytest.raises(SystemExit):
        choose_domain("")
        out, err = capfd.readouterr()
        assert out.strip() == 'Aborted! Canceled template creation!'


