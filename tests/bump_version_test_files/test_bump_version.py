import re
from pathlib import Path
from cookietemple.bump_version.bump_version import bump_template_version


def get_file_versions_after_bump() -> list:
    with open('bump_version_test_files/bump_version_test.py', 'r') as bumped_file:
        data = bumped_file.read()
        bumped_versions = re.findall("[0-9]+.[0-9]+.[0-9]+", data)

    return bumped_versions


def test_bump_version() -> None:
    """
    This function test the bump version function with various cases in a test file
    """
    bump_template_version('5.5.5', Path('../tests/bump_version_test_files'))
    assert get_file_versions_after_bump() == ['5.5.5'] + ['0.0.0'] + ['5.5.5' for _ in range(3)] + \
        ['0.0.0' for _ in range(3)] + ['5.5.5'] + ['0.0.0']

    bump_template_version('0.0.0', Path('../tests/bump_version_test_files'))
