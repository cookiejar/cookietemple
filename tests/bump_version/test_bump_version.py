import re
import pytest
import os
from pathlib import Path
from click.testing import CliRunner

from cookietemple.bump_version.bump_version import VersionBumper
from cookietemple.cookietemple_cli import bump_version


@pytest.fixture
def valid_version_bumpers():
    """
    Return a list of valid versions for bumping executed one after another (Order matters!).
    """
    return ['12.12.12', '12.12.13', '12.13.0-SNAPSHOT', '12.13.9', '13.0.0', '13.0.40', '100.0.0', '100.0.1-SNAPSHOT', '100.0.1']


def test_bump_version(mocker, valid_version_bumpers) -> None:
    """
    Test bump version in white- and blacklisted files.
    NOTE: If you edit the test files, you must edit the ranges here to (initially versions[0-9] are bumped, the rest should not be bumped)
    """
    mocker.patch.object(Path, 'cwd', autospec=True)
    Path.cwd.return_value = str(os.path.abspath(os.path.dirname(__file__)))
    version_bumper = VersionBumper()

    for version in valid_version_bumpers:
        version_bumper.bump_template_version(version, Path(str(os.path.abspath(os.path.dirname(__file__)))))
        versions_whitelisted, versions_blacklisted = get_file_versions_after_bump(Path.cwd())

        assert (all(versions_whitelisted[i] == version for i in range(10)) and
                all(versions_whitelisted[i] != version for i in range(10, len(versions_whitelisted)))) and \
               (all(versions_blacklisted[i] == version for i in range(10)) and
                all(versions_blacklisted[i] != version for i in range(10, len(versions_blacklisted))))
    reset_after_bump_test(Path.cwd())


def test_same_version_throws_error() -> None:
    """
    Call bump-version with the same version as the current results in error.
    """
    runner = CliRunner()
    result = runner.invoke(bump_version, ['0.0.0', str(os.path.abspath(os.path.dirname(__file__)))])

    assert result.exit_code != 0


def test_bad_dir_throws_error() -> None:
    """
    Call bump-version in a directory not containing a cookietemple.cfg file results in error.
    """
    runner = CliRunner()
    result = runner.invoke(bump_version, ['0.0.0', str(os.path.abspath(os.path.dirname(__file__))) + '/bump_version_test_files'])

    assert result.exit_code != 0


def get_file_versions_after_bump(cwd: Path) -> (list, list):
    """
    Read all version numbers and test whether they were correctly bumped (or not bumped if tagged/not matched)
    :param cwd: Current Working Dir
    :return: List of all regex matches, one for whitelisted one for blacklisted
    """
    valid_version_regex = r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)'

    with open(f'{cwd}/bump_version_test_files/bump_test_file_whitelisting', 'r') as bumped_file_whitelisted:
        bumped_data = bumped_file_whitelisted.read()
        bumped_versions_whitelisted = re.findall(valid_version_regex, bumped_data)

    with open(f'{cwd}/bump_version_test_files/bump_test_file_blacklisting', 'r') as bumped_file_blacklisted:
        bumped_data = bumped_file_blacklisted.read()
        bumped_versions_blacklisted = re.findall(valid_version_regex, bumped_data)

    return bumped_versions_whitelisted, bumped_versions_blacklisted


def reset_after_bump_test(cwd: Path):
    """
    Reset test files to initial state with initial version number for further testing.
    :param cwd: Current Work Dir
    """
    version_bumper = VersionBumper()
    version_bumper.replace(f'{str(cwd)}/bump_version_test_files/bump_test_file_whitelisting', '0.0.0', 'bumpversion_files_whitelisted')
    version_bumper.replace(f'{str(cwd)}/bump_version_test_files/bump_test_file_blacklisting', '0.0.0', 'bumpversion_files_blacklisted')
    version_bumper.replace(f'{str(cwd)}/cookietemple.cfg', '0.0.0', 'bumpversion_files_whitelisted')
