import os
from subprocess import Popen
from typing import List

import requests
from pkg_resources import parse_version
from rich import print

from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.lint.template_linter import TemplateLinter, files_exist_linting, GetLintingFunctionsMeta

CWD = os.getcwd()


class CliPythonLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, is_create, skip_external):
        super().lint_project(self, self.methods)

        # Call autopep8, if needed
        if is_create:
            print('[bold blue]Running autopep8 to fix pep8 issues in place')
            autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'],
                             universal_newlines=True, shell=False, close_fds=True)
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()
        elif skip_external:
            pass
        elif cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                          question='Do you want to run autopep8 to fix pep8 issues?',
                                                          default='n'):
            print('[bold blue]Running autopep8 to fix pep8 issues in place')
            autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'],
                             universal_newlines=True, shell=False, close_fds=True)
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def check_dependencies_not_outdated(self) -> bool:
        """
        Check that every dependency from project's requirements.txt is the latest version available at PyPi.

        :return Bool flag that shows code execution went right (used for testing purposes)
        """

        def check_dependencies(filename: str) -> None:
            """
            Check for a given file whether no dependencies are outdated.
            :param filename: Name of the dependency file to parse (either requirements.txt or requirements_dev.txt)
            """
            with open(f'{self.path}/{filename}') as req_file:
                dependencies = [line[:-1].split('==') for line in req_file]
            for dependency in dependencies:
                if len(dependency) == 2:
                    _check_pip_package(dependency[0], dependency[1])

        def _check_pip_package(pip_dependency_name, pip_dependency_version) -> None:
            """
            Query PyPi package information.
            Sends a HTTP GET request to the PyPi remote API.

            :param pip_dependency_name: The name of the dependency
            :param pip_dependency_version: Dependency version used by the user's project
            """
            pip_api_url = f'https://pypi.python.org/pypi/{pip_dependency_name}/json'
            try:
                response = requests.get(pip_api_url, timeout=10)
            except requests.exceptions.Timeout:
                self.warned.append(('cli-python-2', f'PyPi API timed out: {pip_api_url}'))
            except requests.exceptions.ConnectionError:
                self.warned.append(('cli-python-2', f'PyPi API Connection error: {pip_api_url}'))
            else:
                if response.status_code == 200:
                    pip_dep_json = response.json()
                    latest_dependency_version = pip_dep_json['info']['version']
                    if parse_version(pip_dependency_version) < parse_version(latest_dependency_version):
                        self.warned.append(('cli-python-2', f'Version {pip_dependency_version} of {pip_dependency_name} is not the latest available: '
                        f'{latest_dependency_version}'))  # noqa: E128
                else:
                    self.failed.append(('cli-python-2', f'Could not find pip dependency using the PyPi API: {pip_dependency_name}=={pip_dependency_version}'))

        # check general dependencies
        check_dependencies('requirements.txt')
        # check development dependencies
        check_dependencies('requirements_dev.txt')
        return True

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
        files_warn_ifexists: List[str] = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='cli-python')


class CliJavaLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, skip_external):
        super().lint_project(self, self.methods)

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
        files_fail_ifexists: List[str] = [

        ]
        files_warn_ifexists: List[str] = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='cli-java')
