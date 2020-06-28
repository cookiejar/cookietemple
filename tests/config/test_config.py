from click.testing import CliRunner
from pathlib import Path

from cookietemple.config.config import ConfigCommand
from cookietemple.cookietemple_cli import config
from cookietemple.util.yaml_util import load_yaml_file
from cookietemple.create.github_support import decrypt_pat


def test_general_settings(mocker):
    runner = CliRunner()

    with runner.isolated_filesystem():
        mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
        ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'

        result = runner.invoke(config, ['general'], input='Homer Simpson\nsimpson@hotmail.com\nhomergithub')
        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)

        assert result.exit_code == 0 and general_settings['full_name'] == 'Homer Simpson' and general_settings['email'] == 'simpson@hotmail.com' \
            and general_settings['github_username'] == 'homergithub' and 'pat' not in general_settings


def test_pat_setting_requires_general_settings(mocker):
    runner = CliRunner()

    with runner.isolated_filesystem():
        mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
        ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
        mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
        ConfigCommand.KEY_PAT_FILE = f'{str(Path.cwd())}/.cookietemple_key_test'

        # invoked when no cfg file exists, so the user should be prompted for general settings first
        result = runner.invoke(config, ['pat'], input='Homer Simpson\nsimpson@hotmail.com\nhomergithub\ny\nspringfieldToken1234\ny')
        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
        decrpyted_pat = decrypt_pat()

        assert result.exit_code == 0 and general_settings['full_name'] == 'Homer Simpson' and general_settings['email'] == 'simpson@hotmail.com' \
            and general_settings['github_username'] == 'homergithub' and decrpyted_pat == 'springfieldToken1234'


def test_canceling_pat_set_will_not_overwrite(mocker):
    runner = CliRunner()

    with runner.isolated_filesystem():
        mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
        ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
        mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
        ConfigCommand.KEY_PAT_FILE = f'{str(Path.cwd())}/.cookietemple_key_test'

        # invoked for the first time
        result = runner.invoke(config, ['pat'], input='Homer Simpson\nsimpson@hotmail.com\nhomergithub\ny\nspringfieldToken1234\ny')
        # invoke pat config vor second time but cancel update
        result_sec = runner.invoke(config, ['pat'], input='y\nmrburnshijackesyourtoken111\nn')

        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
        decrpyted_pat = decrypt_pat()

        # ensure nothing changed
        assert result.exit_code == 0 and result_sec.exit_code == 1 and general_settings['full_name'] == 'Homer Simpson' and \
            general_settings['email'] == 'simpson@hotmail.com' and general_settings['github_username'] == 'homergithub' and \
            decrpyted_pat == 'springfieldToken1234'


def test_all_settings(mocker):
    runner = CliRunner()

    with runner.isolated_filesystem():
        mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
        ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
        mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
        ConfigCommand.KEY_PAT_FILE = f'{str(Path.cwd())}/.cookietemple_key_test'

        result = runner.invoke(config, ['all'], input='Homer Simpson\nsimpson@hotmail.com\nhomergithub\ny\nspringfieldToken1234\ny')
        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
        decrpyted_pat = decrypt_pat()

        assert result.exit_code == 0 and general_settings['full_name'] == 'Homer Simpson' and \
            general_settings['email'] == 'simpson@hotmail.com' and general_settings['github_username'] == 'homergithub' and \
            decrpyted_pat == 'springfieldToken1234'


def test_all_settings_update(mocker):
    runner = CliRunner()

    with runner.isolated_filesystem():
        mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
        ConfigCommand.CONF_FILE_PATH = f'{str(Path.cwd())}/cookietemple_test_cfg.yml'
        mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
        ConfigCommand.KEY_PAT_FILE = f'{str(Path.cwd())}/.cookietemple_key_test'

        # invoked for the first time
        result = runner.invoke(config, ['all'], input='Homer Simpson\nsimpson@hotmail.com\nhomergithub\ny\nspringfieldToken1234\ny')
        result_sec = runner.invoke(config, ['all'], input='Grandpa Simpson\noldman@hotmail.com\ngrandpagithub\ny\ngrandpaToken123\ny')

        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
        decrpyted_pat = decrypt_pat()

        # ensure all attributes are updated
        assert result.exit_code == 0 and result_sec.exit_code == 0 and general_settings['full_name'] == 'Grandpa Simpson' and \
            general_settings['email'] == 'oldman@hotmail.com' and general_settings['github_username'] == 'grandpagithub' and \
            decrpyted_pat == 'grandpaToken123'
