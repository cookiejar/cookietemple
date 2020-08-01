import os
from subprocess import Popen
from rich import print

from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.lint.template_linter import TemplateLinter, files_exist_linting, GetLintingFunctionsMeta

CWD = os.getcwd()


class LibCppLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

        # Call autopep8, if needed
        if cookietemple_questionary_or_dot_cookietemple(function='confirm',
                                                          question='Do you want to run autopep8 to fix pep8 issues?',
                                                          default='n'):
            print('[blue]Running autopep8 to fix pep8 issues in place')
            autopep8 = Popen(['autopep8', self.path, '--recursive', '--in-place', '--pep8-passes', '2000'],
                             universal_newlines=True, shell=False, close_fds=True)
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def cpp_files_exist(self) -> None:
        """
        Checks a given project directory for required files.
        Iterates through the templates's directory content and checkmarks files for presence.
        Files that **must** be present::
            'CMakeLists.txt',
        Files that *should* be present::
            '.clang-format'
            '.clang-tidy'
            '.github/workflows/build_windows.yml',
            '.github/workflows/build_linux.yml',
            '.github/workflows/build_macos.yml',
            '.github/workflows/release.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            none
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['CMakeLists.txt'],
        ]
        files_warn = [
            [os.path.join('.clang-format')],
            [os.path.join('.clang-tidy')],
            [os.path.join('.github', 'workflows', 'build_windows.yml')],
            [os.path.join('.github', 'workflows', 'build_linux.yml')],
            [os.path.join('.github', 'workflows', 'build_macos.yml')],
            [os.path.join('.github', 'workflows', 'release.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [
        ]
        files_warn_ifexists = [
        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='lib-cpp')


