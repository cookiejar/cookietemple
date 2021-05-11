import json
import logging
import sys
import urllib
from subprocess import PIPE, Popen, check_call
from urllib.error import HTTPError, URLError

from pkg_resources import parse_version
from rich import print

import cookietemple
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple

log = logging.getLogger(__name__)


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
            if cookietemple_questionary_or_dot_cookietemple(
                function="confirm", question="Do you want to upgrade?", default="y"
            ):
                UpgradeCommand.upgrade_cookietemple()

    @classmethod
    def check_cookietemple_latest(cls) -> bool:
        """
        Checks whether the locally installed version of cookietemple is the latest available on PyPi.

        :return: True if locally version is the latest or PyPI is inaccessible, false otherwise
        """
        latest_local_version = cookietemple.__version__
        sliced_local_version = (
            latest_local_version[:-9] if latest_local_version.endswith("-SNAPSHOT") else latest_local_version
        )
        log.debug(f"Latest local cookietemple version is: {latest_local_version}.")
        log.debug("Checking whether a new cookietemple version exists on PyPI.")
        try:
            # Retrieve info on latest version
            # Adding nosec (bandit) here, since we have a hardcoded https request
            # It is impossible to access file:// or ftp://
            # See: https://stackoverflow.com/questions/48779202/audit-url-open-for-permitted-schemes-allowing-use-of-file-or-custom-schemes
            req = urllib.request.Request("https://pypi.org/pypi/cookietemple/json")  # nosec
            with urllib.request.urlopen(req, timeout=1) as response:  # nosec
                contents = response.read()
                data = json.loads(contents)
                latest_pypi_version = data["info"]["version"]
        except (HTTPError, TimeoutError, URLError):
            print(
                "[bold red]Unable to contact PyPI to check for the latest cookietemple version. Do you have an internet connection?"
            )
            # Returning true by default, since this is not a serious issue
            return True

        if parse_version(sliced_local_version) > parse_version(latest_pypi_version):
            print(
                f"[bold yellow]Installed version {latest_local_version} of cookietemple is newer than the latest release {latest_pypi_version}!"
                f" You are running a nightly version and features may break!"
            )
        elif parse_version(sliced_local_version) == parse_version(latest_pypi_version):
            return True
        else:
            print(
                f"[bold red]Installed version {latest_local_version} of cookietemple is outdated. Newest version is {latest_pypi_version}!"
            )
            return False

        return False

    @classmethod
    def upgrade_cookietemple(cls) -> None:
        """
        Calls pip as a subprocess with the --upgrade flag to upgrade cookietemple to the latest version.
        """
        log.debug("Attempting to upgrade cookietemple via    pip install --upgrade cookietemple .")
        if not UpgradeCommand.is_pip_accessible():
            sys.exit(1)
        try:
            check_call([sys.executable, "-m", "pip", "install", "--upgrade", "cookietemple"])
        except Exception as e:
            print("[bold red]Unable to upgrade cookietemple")
            print(f"[bold red]Exception: {e}")

    @classmethod
    def is_pip_accessible(cls) -> bool:
        """
        Verifies that pip is accessible and in the PATH.

        :return: True if accessible, false if not
        """
        log.debug("Verifying that pip is accessible.")
        pip_installed = Popen(["pip", "--version"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        (git_installed_stdout, git_installed_stderr) = pip_installed.communicate()
        if pip_installed.returncode != 0:
            log.debug("Pip was not accessible!")
            print("[bold red]Unable to find 'pip' in the PATH. Is it installed?")
            print("[bold red]Run command was [green]'pip --version '")
            return False

        return True
