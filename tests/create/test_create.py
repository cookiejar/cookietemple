import pytest
import pytest_mock
from io import StringIO
from pathlib import Path
from distutils.dir_util import copy_tree


from cookietemple.create.create import choose_domain
from cookietemple.create.create_config import (TEMPLATE_STRUCT,delete_dir_tree)

@pytest.fixture
def valid_domains():
    return ['cli', 'gui', 'web']


def posix_path_super_dir(path):
    return [Path(f"{path}/MANIFEST.in"),Path(f"{path}/.editorconfig"),Path(f"{path}/Makefile"),Path(f"{path}/README.rst"),
            Path(f"{path}/tests"),Path(f"{path}/readthedocs.yml"),Path(f"{path}/tox.ini"),Path(f"{path}/requirements_dev.txt"),
            Path(f"{path}/.travis.yml"),Path(f"{path}/.gitignore"),Path(f"{path}/slug"),Path(f"{path}/.github"),
            Path(f"{path}/setup.py"),Path(f"{path}/.cookietemple"),Path(f"{path}/CODE_OF_CONDUCT.rst"),Path(f"{path}/docs"),
            Path(f"{path}/Dockerfile"),Path(f"{path}/requirements.txt"),Path(f"{path}/setup.cfg"),Path(f"{path}/CHANGELOG.rst"),
            Path(f"{path}/CONTRIBUTING.rst"),Path(f"{path}/LICENSE"),Path(f"{path}/AUTHORS.rst"),Path(f"{path}/.dependabot"),]



# test creation of a simple cli python template
#TODO: USE LINTING (LIKE NF CORE TOOLS) TO TEST COOKIECUTTER WITH EXTRA_CONTENT
def test_choose_domain_cli(monkeypatch,valid_domains,tmp_path):
    prompt = StringIO(f"{valid_domains[0]}\npython\nname\nmail\naccname\nprojectname\nslug\ndesc\n0.1"
                      f"\nMIT\npypi\nClick\npytest\nYes")
    monkeypatch.setattr('sys.stdin', prompt)
    choose_domain("")
    copy_tree(f'{Path.cwd()}/slug', str(tmp_path))
    delete_dir_tree(Path(f"{Path.cwd()}/slug"))
    assert list(tmp_path.iterdir()) == posix_path_super_dir(tmp_path)
