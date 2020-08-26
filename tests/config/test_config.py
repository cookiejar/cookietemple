import os
import sys
import pytest

from cookietemple.config.config import ConfigCommand
from cookietemple.common.load_yaml import load_yaml_file
from cookietemple.create.github_support import decrypt_pat


def test_general_settings(mocker, tmp_path):
    """
    Test cookietemple config general

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer Simpson\nsimpson@gmail.com\nhomergithub\n"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'

    ConfigCommand.config_general_settings()
    general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)

    assert general_settings['full_name'] == 'Homer Simpson' and general_settings['email'] == 'simpson@gmail.com' \
           and general_settings['github_username'] == 'homergithub' and 'pat' not in general_settings


def test_pat_setting_all(mocker, tmp_path):
    """
    Test cookietemple config all

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer Simpson\nsimpson@gmail.com\nhomergithub\ny\nspringfieldToken1234\ny"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'
    mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
    ConfigCommand.KEY_PAT_FILE = f'{str(os.getcwd())}/.cookietemple_key_test'

    # invoked when no cfg file exists, so the user should be prompted for general settings first
    ConfigCommand.all_settings()
    general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
    decrpyted_pat = decrypt_pat()

    assert general_settings['full_name'] == 'Homer Simpson' and general_settings['email'] == 'simpson@gmail.com' \
           and general_settings['github_username'] == 'homergithub' and decrpyted_pat == 'springfieldToken1234'


def test_canceling_pat_set_will_not_overwrite(mocker, tmp_path):
    """
    Canceling PAT update should not change it

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer Simpson\nsimpson@gmail.com\nhomergithub\ny\nspringfieldToken1234\ny"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    os.write(w, b"y\nmrburnshijackesyourtoken111\nn")
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'
    mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
    ConfigCommand.KEY_PAT_FILE = f'{str(os.getcwd())}/.cookietemple_key_test'

    with pytest.raises(SystemExit):
        ConfigCommand.config_pat()
        ConfigCommand.config_pat()
        general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
        decrpyted_pat = decrypt_pat()

        assert general_settings['full_name'] == 'Homer Simpson' and general_settings['email'] == 'simpson@hotmail.com' \
            and general_settings['github_username'] == 'homergithub' and decrpyted_pat == 'springfieldToken1234'


def test_all_settings_update(mocker, tmp_path):
    """
    Test whether all items get updated

    This tests redirects standard input (basically recreating the pipe operator from bash) because when using questionary, one cannot pass input from stdin.
    """
    input_str = b"Homer Simpson\nsimpson@gmail.com\nhomergithub\ny\nspringfieldToken1234\ny"
    r, w = os.pipe()
    os.dup2(r, sys.stdin.fileno())
    os.write(w, input_str)
    os.write(w, b"Grandpa Simpson\noldman@hotmail.com\ngrandpagithub\ny\ngrandpaToken123\ny")
    mocker.patch.object(os.path, 'isdir', autospec=True)
    os.path.isdir.return_value = True
    mocker.patch.object(os, 'getcwd', autospec=True)
    os.getcwd.return_value = str(tmp_path)
    mocker.patch.object(ConfigCommand, 'CONF_FILE_PATH', autospec=True)
    ConfigCommand.CONF_FILE_PATH = f'{str(os.getcwd())}/cookietemple_test_cfg.yml'
    mocker.patch.object(ConfigCommand, 'KEY_PAT_FILE', autospec=True)
    ConfigCommand.KEY_PAT_FILE = f'{str(os.getcwd())}/.cookietemple_key_test'

    ConfigCommand.all_settings()
    ConfigCommand.all_settings()

    general_settings = load_yaml_file(ConfigCommand.CONF_FILE_PATH)
    decrpyted_pat = decrypt_pat()

    # ensure all attributes are updated
    assert general_settings['full_name'] == 'Grandpa Simpson' and general_settings['email'] == 'oldman@hotmail.com' \
        and general_settings['github_username'] == 'grandpagithub' and decrpyted_pat == 'grandpaToken123'
