import os
from subprocess import Popen

import click

from cookietemple.lint.template_linter import TemplateLinter, files_exist_linting

CWD = os.getcwd()


class CliPythonLint(TemplateLinter):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, is_create):
        methods = ['python_files_exist']
        super().lint_project(self, methods)

        # Call autopep8, if needed
        if is_create:
            click.echo(click.style('Running autopep8 to fix pep8 issues in place', ))
            autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'], universal_newlines=True, shell=False,
                             close_fds=True)
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()
        elif click.confirm('Do you want to run autopep8 to fix pep8 issues?'):
            click.echo(click.style('Running autopep8 to fix pep8 issues in place', ))
            autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'], universal_newlines=True, shell=False,
                             close_fds=True)
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def python_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
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
            [os.path.join('.github', 'workflows', 'run_tox_testsuite.yml')],
            [os.path.join('.github', 'workflows', 'run_flake8_linting.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
            '__pycache__'
        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='cli-python')


class CliJavaLint(TemplateLinter):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        methods = ['java_files_exist']
        super().lint_project(self, methods)

    def java_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'build.gradle',
            'settings.gradle',
        Files that *should* be present::
            '.github/workflows/build_deploy.yml',
            '.github/workflows/run_checkstyle.yml',
            '.github/workflows/tox_tests.yml',
            'gradle/wrapper/gradle-wrapper.jar',
            'gradle/wrapper/gradle-wrapper.properties',
            'gradlew',
            'gradlew.bat',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            none
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['build.gradle'],
            ['settings.gradle'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'build_deploy.yml')],
            [os.path.join('.github', 'workflows', 'run_checkstyle.yml')],
            [os.path.join('.github', 'workflows', 'run_tests.yml')],
            [os.path.join('gradle', 'wrapper', 'gradle-wrapper.jar')],
            [os.path.join('gradle', 'wrapper', 'gradle-wrapper.properties')],
            [os.path.join('gradlew')],
            [os.path.join('gradlew.bat')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [

        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='cli-java')

