import os
from typing import List

from cookietemple.lint.template_linter import ConfigLinter, GetLintingFunctionsMeta, TemplateLinter, files_exist_linting

CWD = os.getcwd()


class LibCppLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
    def __init__(self, path):
        super().__init__(path)

    def lint(self):
        super().lint_project(self, self.methods)

    def check_sync_section(self) -> bool:
        """
        Check the sync_files_blacklisted section containing every required file!
        """
        config_linter = ConfigLinter(f"{self.path}/cookietemple.cfg", self)
        result = config_linter.check_section(
            section_items=config_linter.parser.items("sync_files_blacklisted"),
            section_name="sync_files_blacklisted",
            main_linter=self,
            blacklisted_sync_files=[[("changelog", "CHANGELOG.rst")], -1],
            error_code="lib-cpp-2",
            is_sublinter_calling=True,
        )
        if result:
            self.passed.append(("lib-cpp-2", "All required sync blacklisted files are configured!"))
        else:
            self.failed.append(("lib-cpp-2", "Blacklisted sync files section misses some required files!"))
        return result

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
            ["CMakeLists.txt"],
        ]
        files_warn = [
            [os.path.join(".clang-format")],
            [os.path.join(".clang-tidy")],
            [os.path.join(".github", "workflows", "build_windows.yml")],
            [os.path.join(".github", "workflows", "build_linux.yml")],
            [os.path.join(".github", "workflows", "build_macos.yml")],
            [os.path.join(".github", "workflows", "release.yml")],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists: List[str] = []
        files_warn_ifexists: List[str] = []

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, handle="lib-cpp")
