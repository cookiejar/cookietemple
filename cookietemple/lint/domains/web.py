import os
from subprocess import Popen
from typing import List

from rich import print

from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.lint.template_linter import ConfigLinter, GetLintingFunctionsMeta, TemplateLinter, files_exist_linting

CWD = os.getcwd()


class WebWebsitePythonLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, is_create, skip_external):
        super().lint_project(self, self.methods)

        # Call autopep8, if needed
        if is_create:
            print("[blue]Running autopep8 to fix pep8 issues in place")
            autopep8 = Popen(
                ["autopep8", self.path, "--recursive", "--in-place", "--pep8-passes", "2000"],
                universal_newlines=True,
                shell=False,
                close_fds=True,
            )
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()
        elif skip_external:
            pass
        elif cookietemple_questionary_or_dot_cookietemple(
            function="confirm", question="Do you want to run autopep8 to fix pep8 issues?", default="n"
        ):
            print("[blue]Running autopep8 to fix pep8 issues in place")
            autopep8 = Popen(
                ["autopep8", self.path, "--recursive", "--in-place", "--pep8-passes", "2000"],
                universal_newlines=True,
                shell=False,
                close_fds=True,
            )
            (autopep8_stdout, autopep8_stderr) = autopep8.communicate()

    def check_sync_section(self) -> bool:
        """
        Check the sync_files_blacklisted section containing every required file!
        """
        config_linter = ConfigLinter(f"{self.path}/cookietemple.cfg", self)
        result = config_linter.check_section(
            section_items=config_linter.parser.items("sync_files_blacklisted"),
            section_name="sync_files_blacklisted",
            main_linter=self,
            blacklisted_sync_files=[
                [
                    ("requirements", "requirements.txt"),
                    ("requirements_dev", "requirements_dev.txt"),
                    ("changelog", "CHANGELOG.rst"),
                ],
                -1,
            ],
            error_code="web-python-2",
            is_sublinter_calling=True,
        )
        if result:
            self.passed.append(("web-python-2", "All required sync blacklisted files are configured!"))
        else:
            self.failed.append(("web-python-2", "Blacklisted sync files section misses some required files!"))
        return result

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
            ["setup.py"],
            ["setup.cfg"],
            ["MANIFEST.in"],
            ["tox.ini"],
        ]
        files_warn = [
            [os.path.join(".github", "workflows", "build_package.yml")],
            [os.path.join(".github", "workflows", "run_tox_testsuite.yml")],
            [os.path.join(".github", "workflows", "run_flake8_linting.yml")],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = ["__pycache__"]
        files_warn_ifexists: List[str] = []

        files_exist_linting(
            self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle="web-website-python"
        )
