import os
import sys
import click
from pathlib import Path
from cryptography.fernet import Fernet
from ruamel.yaml import YAML

from cookietemple.custom_cookietemple_cli.levensthein_dist import most_similar_command


class ConfigCommand:
    """
    Class for the config command
    """
    # path where the config file is stored for cookietemple
    CONF_FILE_PATH = f'{Path.home()}/cookietemple_conf.yml'

    @staticmethod
    def all_settings() -> None:
        """
        Set general and github settings.
        """
        ConfigCommand.config_general_settings()
        ConfigCommand.config_github_settings(ask_username=False)

    @staticmethod
    def config_general_settings() -> None:
        """
        Set full_name and email for reuse in any project created further on.
        """
        full_name = click.prompt('Please enter your full name', type=str, default='Homer Simpson')
        email = click.prompt('Please enter your personal or work email', type=str, default='homer.simpson@example.com')
        github_username = click.prompt('Please enter your github username', type=str)

        # if the configs exist, just update them
        if os.path.exists(ConfigCommand.CONF_FILE_PATH):
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML(typ='safe')
            settings = yaml.load(path)

            # update the full_name and email
            settings['full_name'] = full_name
            settings['email'] = email
            settings['github_username'] = github_username
            yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

        # the configs don´t exist -> create them
        else:
            settings = {'full_name': full_name, 'email': email, 'github_username': github_username}
            yaml = YAML()
            yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

    @staticmethod
    def config_github_settings(ask_username=True) -> None:
        """
        Set the PAT and Github username for automatic github repo creation.
        """
        # flag that indicates whether the user updates its PAT or not
        token_set, encrypted_pat, github_username = False, '', ''
        if ask_username:
            github_username = click.prompt('Please enter your Github account username ', type=str)

        if click.confirm(click.style('Do you want to configure your GitHub personal access token right now?\nYou can still configure it later '
                                     'by calling ', fg='red') + click.style('cookietemple config github', fg='green')):
            token_set = True
            access_token: str = click.prompt('Please enter your GitHub access token ', type=str, hide_input=True)
            access_token_b = access_token.encode('utf-8')

            # ask for confirmation since this action will delete the PAT irrevocably if the user has not saved it anywhere else
            if not click.confirm(click.style('You´re about to update your personal access token. This action cannot be undone!\n'
                                             'Do you really want to continue?')):
                sys.exit(1)

            # encrypt the given PAT and save the encryption key and encrypted PAT in separate files
            click.echo(click.style('Generating key for encryption.', fg='blue'))
            key = Fernet.generate_key()
            fer = Fernet(key)
            click.echo(click.style('Encrypting personal access token.', fg='blue'))
            encrypted_pat = fer.encrypt(access_token_b)

            # write key
            with open(f'{Path.home()}/.ct_keys', 'wb') as f:
                f.write(key)

        # if the configs exist, just update them
        if os.path.exists(ConfigCommand.CONF_FILE_PATH):
            path = Path(ConfigCommand.CONF_FILE_PATH)
            yaml = YAML(typ='safe')
            settings = yaml.load(path)

            # update username and pat
            if ask_username:
                settings['github_username'] = github_username
            if token_set:
                settings['pat'] = encrypted_pat
            if settings:
                yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))

        # the configs don´t exist -> create them (maybe in case of pub template creation)
        else:
            # both username and PAT were set
            if ask_username and token_set:
                settings = {'github_username': github_username, 'pat': encrypted_pat}
                yaml = YAML()
                yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))
            # only the PAT was set
            elif token_set:
                settings = {'pat': encrypted_pat}
                yaml = YAML()
                yaml.dump(settings, Path(ConfigCommand.CONF_FILE_PATH))
            # some weird user behaviour catching
            else:
                click.echo(click.style('Please set your github username and personal access token in order to push to a github repo by calling ',
                                       fg='red') + click.style('cookietemple config github', fg='green'))

    @staticmethod
    def similar_handle(section: str) -> None:
        """
        Try to use/suggest a similar handle if user missspelled it.
        :param section: The handle inputted by the user.
        """
        com_list, action = most_similar_command(section.lower(), {'general', 'github', 'all'})
        # use best match
        if len(com_list) == 1 and action == 'use':
            click.echo(click.style(f'Unknown handle {section}. Will use best match {com_list[0]}.\n', fg='blue'))
            ConfigCommand.handle_switcher().get(com_list[0], lambda: 'Invalid handle!')()
        # suggest best match
        elif len(com_list) == 1 and action == 'suggest':
            click.echo(click.style(f'Unknown handle {section}. Did you mean {com_list[0]}?', fg='blue'))
            sys.exit(1)
            # multiple best matches
        elif len(com_list) > 1:
            nl = '\n'
            click.echo(click.style(f'Unknown handle \'{section}\'.\nMost similar handles are:', fg='red') + click.style(f'{nl}{nl.join(sorted(com_list))}',
                                                                                                                        fg='green'))
        else:
            # unknown handle and no best match found
            click.echo(
                click.style('Unknown handle ', fg='red') + click.style(section, fg='green') + click.style(' See cookietemple --help for info on valid handles',
                                                                                                          fg='red'))

    @staticmethod
    def handle_switcher() -> dict:
        """
        Just a helper to switch between handles.
        :return: The switcher with all handles.
        """
        switcher = {
            'all': ConfigCommand.all_settings,
            'general': ConfigCommand.config_general_settings,
            'github': ConfigCommand.config_github_settings
        }
        return switcher
