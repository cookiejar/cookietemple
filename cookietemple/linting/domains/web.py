import os
import re
from subprocess import Popen
import configparser

import click

from cookietemple.linting.TemplateLinter import TemplateLinter, files_exist_linting

CWD = os.getcwd()


class WebWebsitePythonLint(TemplateLinter):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, label):
        methods = ['python_files_exist', 'python_version_consistent']
        super().lint_project(self, methods, label=label)

        # Call autopep8
        click.echo(click.style('Running autopep8 to fix pep8 issues in place', ))
        autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'], universal_newlines=True, shell=False, close_fds=True)
        (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def python_files_exist(self) -> None:
        """
        Checks a given pipeline directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['setup.py'],
            ['setup.cfg'],
            ['MANIFEST.in'],
            ['tox.ini'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'build_package.yml')],
            [os.path.join('.github', 'workflows', 'tox_testsuite.yml')],
            [os.path.join('.github', 'workflows', 'flake8_linting.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists)

    def python_version_consistent(self) -> None:
        """
        This method should check that the version is consistent across all files.
        TODO STRANGE THINGS HAPPENING; TOMORROW FIX
        """
        #parser = configparser.ConfigParser()
        #parser.read(f'{self.path}/cookietemple.cfg')

        #current_version = parser.get('bumpversion', 'current_version')

        #for file, path in parser.items('bumpversion_files'):
            #self.check_python_version_match(path, current_version)

    def check_python_version_match(self, path: str, version: str) -> None:
        """
        Check if the versions in a file are consistent with the current version in the cookietemple.cfg
        :param path: The current file-path to check
        :param version: The current version of the project specified in the cookietemple.cfg file
        """
        with open(path) as file:
            for line in file:
                if "<<COOKIETEMPLE_NO_BUMP>>" not in line:
                    line_version = re.search(r"[0-9]+.[0-9]+.[0-9]+", line)
                    if line_version:
                        line_version = line_version.group(0)
                        if line_version != version:
                            click.echo(click.style(
                                f'Inconsistent version number in {path}\n', fg='blue') + click.style(
                                f'{line} should be {version}', fg='red'))



