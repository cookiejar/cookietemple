import os

from cookietemple.lint.template_linter import TemplateLinter, files_exist_linting

CWD = os.getcwd()


class GuiJavaLint(TemplateLinter):
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
            'pom.xml',
        Files that *should* be present::
            '.github/workflows/build_package.yml',
            '.github/workflows/build_docs.yml',
            '.github/workflows/run_tests.yml',
            '.github/workflows/java_linting.yml',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            none
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ['pom.xml'],
        ]
        files_warn = [
            [os.path.join('.github', 'workflows', 'build_docs.yml')],
            [os.path.join('.github', 'workflows', 'run_tests.yml')],
            [os.path.join('.github', 'workflows', 'run_java_linting.yml')],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [

        ]
        files_warn_ifexists = [

        ]

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle='gui-java')
