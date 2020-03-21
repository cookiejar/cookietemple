import os

from cookietemple.linting.TemplateLinter import TemplateLinter, files_exist_linting
from cookietemple.util.dir_util import pf


class CliPythonLint(TemplateLinter):
    def __init__(self):
        super().__init__()

    def lint_python(self):
        methods = ['python_files_exist']
        super().lint_pipeline(self, methods)

    def python_files_exist(self) -> None:
        """Checks a given pipeline directory for required files.
        Iterates through the pipeline's directory content and checkmarks files
        for presence.
        Files that **must** be present::
            'setup.py',
            'setup.cfg',
            'MANIFEST.in',
            'tox.ini',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/publish_package.yml',
            '.github/workflows/tox_testsuite.yml',
            '.github/workflows/flake8.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '__pycache__'
        Raises:
            An AssertionError if .cookietemple is not found found.
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
            [os.path.join('.github', 'workflows', 'publish_package.yml')],
            [os.path.join('.github', 'workflows', 'tox_testsuite.yml')],
            [os.path.join('.github', 'workflows', 'flake8.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        # First - critical files. Check that this is actually a COOKIETEMPLE based project
        if not os.path.isfile(pf(self, '.cookietemple')):
            raise AssertionError('.cookietemple not found!! Is this a COOKIETEMPLE project?')

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists)
