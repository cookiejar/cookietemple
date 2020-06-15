import json
import urllib
import subprocess
import sys
from urllib.error import HTTPError, URLError

import click

import cookietemple


class UpgradeCommand:
    """
    Responsible for checking for newer versions cookietemple and upgrading it if required.
    """
    @staticmethod
    def check_upgrade_cookietemple() -> None:
        """
        Checks whether the locally installed version of cookietemple is the latest.
        If not it prompts whether to upgrade and runs the upgrade command if desired.
        """
        if not UpgradeCommand.check_cookietemple_latest():
            if click.confirm('Do you want to upgrade?'):
                UpgradeCommand.upgrade_cookietemple()

    @classmethod
    def check_cookietemple_latest(cls) -> bool:
        """
        Checks whether the locally installed version of cookietemple is the latest available on PyPi.

        :return: True if locally version is the latest or PyPI is inaccessible, false otherwise
        """
        latest_local_version = cookietemple.__version__
        try:
            # Retrieve info on latest version
            # Adding nosec (bandit) here, since we have a hardcoded https request
            # It is impossible to access file:// or ftp://
            # See: https://stackoverflow.com/questions/48779202/audit-url-open-for-permitted-schemes-allowing-use-of-file-or-custom-schemes
            req = urllib.request.Request('https://pypi.org/pypi/cookietemple/json')  # nosec
            with urllib.request.urlopen(req, timeout=1) as response:  # nosec
                contents = response.read()
                data = json.loads(contents)
                latest_pypi_version = data['info']['version']
        except (HTTPError, TimeoutError, URLError):
            click.echo(click.style('Unable to contact PyPI to check for the latest cookietemple version. Do you have an internet connection?', fg='red'))
            # Returning true by default, since this is not a serious issue
            return True

        if latest_local_version == latest_pypi_version:
            return True
        else:
            click.echo(click.style(f'Installed version {latest_local_version} of cookietemple is outdated. Newest version is {latest_pypi_version}!', fg='red'))
            return False

    @classmethod
    def upgrade_cookietemple(cls) -> None:
        """
        Calls pip as a subprocess with the --upgrade flag to upgrade cookietemple to the latest version.
        """
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'cookietemple'])
        except Exception as e:
            click.echo(click.style('Unable to upgrade cookietemple! Is pip accessible from your PATH?', fg='red'))
            click.echo(click.style(f'Exception: {e}', fg='red'))
