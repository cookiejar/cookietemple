import pytest
# from click.testing import CliRunner


@pytest.fixture()
def get_all_main_commands():
    """
    All core commands COOKIETEMPLE offers currently.
    """
    return ['create', 'info', 'list', 'bump-version', 'lint', 'warp']
