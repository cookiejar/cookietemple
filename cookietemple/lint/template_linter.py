import configparser
import io
import logging
import os
import re
import sys

import rich.markdown
import rich.panel
import rich.progress

from cookietemple.util.dir_util import pf
from cookietemple.util.rich import console

log = logging.getLogger(__name__)


class TemplateLinter(object):
    """Object to hold linting information and results.
    Attributes:
        files (list): A list of files found during the linting process.
        path (str): Path to the project directory.
        failed (list): A list of tuples of the form: `(<error no>, <reason>)`
        passed (list): A list of tuples of the form: `(<passed no>, <reason>)`
        warned (list): A list of tuples of the form: `(<warned no>, <reason>)`
    """

    def __init__(self, path="."):
        self.path = path
        self.files = []
        self.passed = []
        self.warned = []
        self.failed = []

    def lint_project(
        self, calling_class, check_functions: list = None, custom_check_files: bool = False, is_subclass_calling=True
    ) -> None:
        """Main linting function.
        Takes the template directory as the primary input and iterates through
        the different linting checks in order. Collects any warnings or errors
        and returns summary at completion. Raises an exception if there is a
        critical error that makes the rest of the tests pointless (eg. no
        project script). Results from this function are printed by the main script.

        :param calling_class: The class that calls the function -> used to get the class methods, which are the linting methods
        :param check_functions: List of functions of the calling class that should be checked. If not set, the default TemplateLinter check functions are called
        :param custom_check_files: Set to true if TemplateLinter check_files_exist should not be run
        :param is_subclass_calling: Indicates whether a domain specific linter calls the linting or not
        """
        # Called on its own, so not from a subclass -> run general linting
        if check_functions is None:
            # Fetch all general linting functions
            check_functions = [
                func
                for func in dir(TemplateLinter)
                if (callable(getattr(TemplateLinter, func)) and not func.startswith("_"))
            ]
            # Remove internal functions
            check_functions = list(
                set(check_functions).difference({"lint_project", "print_results", "check_version_match"})
            )
            log.debug(f"Linting functions of general linting are:\n {check_functions}")
        # Some templates (e.g. latex based) do not adhere to the common programming based templates and therefore do not need to check for e.g. docs
        if custom_check_files:
            check_functions.remove("check_files_exist")

        progress = rich.progress.Progress(
            "[bold green]{task.description}",
            rich.progress.BarColumn(bar_width=None),
            "[bold yellow]{task.completed} of {task.total}[reset] [bold green]{task.fields[func_name]}",
        )
        with progress:
            lint_progress = progress.add_task(
                "Running lint checks", total=len(check_functions), func_name=check_functions
            )
            for fun_name in check_functions:
                log.debug(f"Running linting function: {fun_name}")
                progress.update(lint_progress, advance=1, func_name=fun_name)
                if fun_name == "check_files_exist":
                    getattr(calling_class, fun_name)(is_subclass_calling)
                else:
                    getattr(calling_class, fun_name)()

    def check_files_exist(self, is_subclass_calling=True):
        """Checks a given project directory for required files.
        Iterates through the project's directory content and checkmarks files
        for presence.
        Files that **must** be present::
            'Dockerfile',
            'cookietemple.cfg'
            'Makefile'
            'README.rst'
            '[LICENSE, LICENSE.md, LICENCE, LICENCE.md]'
            'docs/index.rst'
            'docs/readme.rst'
            'docs/installation.rst'
            'docs/usage.rst'
        Files that *should* be present::
            '.gitignore',
            '.github/ISSUE_TEMPLATE/bug_report.md',
            '.github/ISSUE_TEMPLATE/general_question.md',
            '.github/ISSUE_TEMPLATE/feature_request.md',
            '.github/pull_request.md',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            none
        Raises:
            An AssertionError if .cookietemple.yml is not found found.
        """

        # NB: Should all be files, not directories
        # List of lists. Passes if any of the files in the sublist are found.
        files_fail = [
            ["Dockerfile"],
            ["cookietemple.cfg"],
            ["Makefile"],
            ["README.rst"],
            ["LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md"],  # NB: British / American spelling
            [os.path.join("docs", "index.rst")],
            [os.path.join("docs", "readme.rst")],
            [os.path.join("docs", "installation.rst")],
            [os.path.join("docs", "usage.rst")],
        ]

        files_warn = [
            [".gitignore"],
            [os.path.join(".github", "ISSUE_TEMPLATE", "bug_report.md")],
            [os.path.join(".github", "ISSUE_TEMPLATE", "feature_request.md")],
            [os.path.join(".github", "ISSUE_TEMPLATE", "general_question.md")],
            [os.path.join(".github", "pull_request_template.md")],
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = []

        files_warn_ifexists = []

        # First - critical files. Check that this is actually a cookietemple based project
        if not os.path.isfile(pf(self, ".cookietemple.yml")):
            print("[bold red] .cookietemple.yml not found! Is this a cookietemple project?")
            sys.exit(1)

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, is_subclass_calling)

    def lint_cookietemple_config(self):
        """
        Lint the cookietemple.cfg file and ensure it meets all requirements for cookietemple.
        """
        config_file_path = os.path.join(self.path, "cookietemple.cfg")
        linter = ConfigLinter(config_file_path, self)
        linter.lint_ct_config_file()

    def check_docker(self):
        """
        Checks that Dockerfile contains the string ``FROM``
        """
        fn = os.path.join(self.path, "Dockerfile")
        with open(fn, "r") as fh:
            content = fh.read()

        # Implicitly also checks if empty.
        if "FROM " in content:
            self.passed.append(("general-2", "Dockerfile check passed"))
            self.dockerfile = [line.strip() for line in content.splitlines()]
            return

        self.failed.append((2, "Dockerfile check failed"))

    def check_cookietemple_todos(self) -> None:
        """
        Go through all template files looking for the string 'TODO COOKIETEMPLE:' or 'COOKIETEMPLE TODO:'
        """
        ignore = [".git"]
        if os.path.isfile(os.path.join(self.path, ".gitignore")):
            with io.open(os.path.join(self.path, ".gitignore"), "rt", encoding="latin1") as file:
                for line in file:
                    ignore.append(os.path.basename(line.strip().rstrip("/")))
        for root, dirs, files in os.walk(self.path):
            # Ignore files
            for ignore_file in ignore:
                if ignore_file in dirs:
                    dirs.remove(ignore_file)
                if ignore_file in files:
                    files.remove(ignore_file)
            for fname in files:
                with io.open(os.path.join(root, fname), "rt", encoding="latin1") as file:
                    for line in file:
                        if any(todostring in line for todostring in ["TODO COOKIETEMPLE:", "COOKIETEMPLE TODO:"]):
                            line = (
                                line.replace("<!--", "")
                                .replace("-->", "")
                                .replace("# TODO COOKIETEMPLE: ", "")
                                .replace("// TODO COOKIETEMPLE: ", "")
                                .replace("TODO COOKIETEMPLE: ", "")
                                .replace("# COOKIETEMPLE TODO: ", "")
                                .replace("// COOKIETEMPLE TODO: ", "")
                                .replace("COOKIETEMPLE TODO: ", "")
                                .strip()
                            )
                            self.warned.append(
                                ("general-3", f"TODO string found in {self._wrap_quotes(fname)}: {line}")
                            )

    def check_no_cookiecutter_strings(self) -> None:
        """
        Verifies that no cookiecutter strings are in any of the files
        """
        for root, _dirs, files in os.walk(self.path):
            for fname in files:
                with io.open(os.path.join(root, fname), "rt", encoding="latin1") as file:
                    if file.name.endswith(".pyc"):
                        continue
                    for line in file:
                        # TODO We should also add some of the more advanced cookiecutter if statements, raw statements etc
                        regex = re.compile(r"{\s?.* cookiecutter.*\s?}")  # noqa W605
                        if regex.search(line):
                            line = f"{line[:50 - len(fname)]}.."
                            self.warned.append(("general-4", f"Cookiecutter string found in '{fname}': {line}"))

    def check_version_consistent(self) -> None:
        """
        This method verifies that the project version is consistent across all files.
        """
        parser = configparser.ConfigParser()
        parser.read(f"{self.path}/cookietemple.cfg")
        sections = ["bumpversion_files_whitelisted", "bumpversion_files_blacklisted"]

        try:
            current_version = parser.get("bumpversion", "current_version")
            cwd = os.getcwd()
            os.chdir(self.path)

            # check if the version matches current version in each listed file (depending on whitelisted or blacklisted)
            for section in sections:
                for _file, path in parser.items(section):
                    self.check_version_match(path, current_version, section)
            os.chdir(cwd)
            # Pass message if there weren't any inconsistencies within the version numbers
            if not any("general-5" in tup[0] for tup in self.failed):
                self.passed.append(("general-5", "Versions were consistent over all files"))
        except configparser.NoOptionError:
            self.failed.append(
                ("general-5", "Cannot check versions due to missing current_version in bumpversion config section!")
            )

    def check_version_match(self, path: str, version: str, section: str) -> None:
        """
        Check if the versions in a file are consistent with the current version in the cookietemple.cfg
        :param path: The current file-path to check
        :param version: The current version of the project specified in the cookietemple.cfg file
        :param section: The current section (blacklisted or whitelisted files)
        """
        with open(path) as file:
            for line in file:
                # if a tag is found and (depending on wether it is a white or blacklisted file) check if the versions are matching
                if (
                    "<<COOKIETEMPLE_NO_BUMP>>" not in line and not section == "bumpversion_files_blacklisted"
                ) or "<<COOKIETEMPLE_FORCE_BUMP>>" in line:
                    line_version = re.search(r"(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)", line)
                    if line_version:
                        line_version = line_version.group(0)  # type: ignore
                        # No match between the current version number and version in source code file
                        if line_version != version:
                            corrected_line = re.sub(r"(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)", version, line)
                            self.failed.append(
                                (
                                    "general-5",
                                    f"Version number don´t match in\n {path}: \n {line.strip()} should be {corrected_line.strip()}",
                                )
                            )

    def print_results(self):
        console.print()
        console.rule("[bold green] LINT RESULTS")
        console.print()
        console.print(
            f"     [bold green][[\u2714]] {len(self.passed):>4} tests passed\n     [bold yellow][[!]] {len(self.warned):>4} tests had warnings\n"
            f"     [bold red][[\u2717]] {len(self.failed):>4} tests failed",
            overflow="ellipsis",
            highlight=False,
        )

        # Helper function to format test links nicely
        def format_result(test_results):
            """
            Given an list of error message IDs and the message texts, return a nicely formatted
            string for the terminal with appropriate ASCII colours.
            """
            results = []
            for eid, msg in test_results:
                results.append(
                    f"1. [https://cookietemple.readthedocs.io/en/latest/lint.html#{eid}]"
                    f"(https://cookietemple.readthedocs.io/en/latest/lint.html#{eid}) : {msg}"
                )
            return rich.markdown.Markdown("\n".join(results))

        if len(self.passed) > 0:
            console.print()
            console.rule("[bold green][[\u2714]] Tests Passed", style="green")
            console.print(rich.panel.Panel(format_result(self.passed), style="green"), overflow="ellipsis")
        if len(self.warned) > 0:
            console.print()
            console.rule("[bold yellow][[!]] Test Warnings", style="yellow")
            console.print(rich.panel.Panel(format_result(self.warned), style="yellow"), overflow="ellipsis")
        if len(self.failed) > 0:
            console.print()
            console.rule("[bold red][[\u2717]] Test Failures", style="red")
            console.print(rich.panel.Panel(format_result(self.failed), style="red"), overflow="ellipsis")

    def _wrap_quotes(self, files):
        if not isinstance(files, list):
            files = [files]
        bfiles = [f"`{file}`" for file in files]

        return " or ".join(bfiles)

    def _strip_ansi_codes(self, string, replace_with=""):
        # https://stackoverflow.com/a/14693789/713980
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

        return ansi_escape.sub(replace_with, string)


def files_exist_linting(
    self,
    files_fail: list,
    files_fail_ifexists: list,
    files_warn: list,
    files_warn_ifexists: list,
    is_subclass_calling=True,
    handle: str = "general",
) -> None:
    """
    Verifies that passed lists of files exist or do not exist.
    Depending on the desired result passing, warning or failing results are appended to the linter object.

    :param self: Linter object
    :param files_fail: list of files which must exist or linting will fail
    :param files_fail_ifexists: list of files which are not allowed to exist or linting will fail
    :param files_warn: list of files which should exist or linting will warn
    :param files_warn_ifexists: list of files which should exist or linting will warn
    :param is_subclass_calling: indicates whether the subclass of TemplateLinter called the linting (specific) or itw as the general linting
    """
    # Files that cause an error if they don't exist
    all_exists = True
    for files in files_fail:
        if not any([os.path.isfile(pf(self, f)) for f in files]):
            all_exists = False
            self.failed.append(("{handle}-1", f"File not found: {self._wrap_quotes(files)}"))
    # flag that indiactes whether all required files exist or not
    if all_exists:
        # called linting from a specific template linter
        if is_subclass_calling:
            self.passed.append((f"{handle}-1", f"All required {handle} specific files were found!"))
        # called as general linting
        else:
            self.passed.append((f"{handle}-1", f"All required {handle} files were found!"))

    # Files that cause a warning if they don't exist
    for files in files_warn:
        if any([os.path.isfile(pf(self, f)) for f in files]):
            # pass cause if a file was found it will be summarised in one "all required files found" statement
            pass
        else:
            self.warned.append((f"{handle}-1", f"File not found: {self._wrap_quotes(files)}"))

    # Files that cause an error if they exist
    for file in files_fail_ifexists:
        if os.path.isfile(pf(self, file)):
            self.failed.append((f"{handle}-1", f"File must be removed: {self._wrap_quotes(file)}"))
        else:
            self.passed.append((f"{handle}-1", f"File not found check: {self._wrap_quotes(file)}"))

    # Files that cause a warning if they exist
    for file in files_warn_ifexists:
        if os.path.isfile(pf(self, file)):
            self.warned.append((f"{handle}-1", f"File should be removed: {self._wrap_quotes(file)}"))
        else:
            self.passed.append((f"{handle}-1", f"File not found check: {self._wrap_quotes(file)}"))


class GetLintingFunctionsMeta(type):
    def get_linting_functions(cls):
        """
        Fetches all specific linting methods and returns them as a list.
        Used for all template specific linters

        :param cls: The specific linting class
        """
        specific_linter_function_names = [
            func for func in dir(cls) if (callable(getattr(cls, func)) and not func.startswith("__"))
        ]
        general_linter_function_names = [
            func
            for func in dir(TemplateLinter)
            if (callable(getattr(TemplateLinter, func)) and not func.startswith("__"))
        ]
        cls_only_funcs = list(set(specific_linter_function_names) - set(general_linter_function_names))
        cls_only_funcs.remove(
            "lint"
        )  # remove 'lint', since we only want the newly defined methods and not the method itself

        return cls_only_funcs

    def __call__(self, *args, **kwargs):
        # create the new class as normal
        cls = type.__call__(self, *args)

        # set the methods attribute to a list of all specific linting functions
        setattr(cls, "methods", self.get_linting_functions())  # noqa: B010

        return cls


class ConfigLinter:
    def __init__(self, path, linter_ctx: TemplateLinter):
        self.config_file_path = path
        self.parser = configparser.ConfigParser()
        self.linter_ctx = linter_ctx
        self.parser.read(f"{self.config_file_path}")

    def lint_ct_config_file(self):
        """
        Lint the sections from the cookietemple.cfg file applying the following rules:

        1.) Every config file should have at least the following sections:
            bumpversion, bumpversion_files_whitelisted, bumpversion_files_blacklisted,
            sync_files_blacklisted, sync_level

        2.) 'bumpversion' should contain a 'current_version' value (the project's current version)

        3.) 'bumpversion_files_whitelisted' should contain at least the '.cookietemple.yml' file

        4.) 'sync_level' should contain a 'ct_sync_level' value (and this value should be one of either 'patch', 'minor' or 'major')

        5.) 'sync' should contain a 'sync_enabled' value (and this value should be one of either "True, true, Yes, yes, Y, y or False, false, No, no, N, n")
        """
        no_section_missing = self.check_missing_sections(self.parser.sections())
        if no_section_missing:
            lint_section_flag = True
            lint_section_flag &= self.check_section(self.parser.items("bumpversion"), "bumpversion", self.linter_ctx)
            lint_section_flag &= self.check_section(
                self.parser.items("bumpversion_files_whitelisted"), "bumpversion_files_whitelisted", self.linter_ctx
            )
            lint_section_flag &= self.check_section(self.parser.items("sync_level"), "sync_level", self.linter_ctx)
            lint_section_flag &= self.check_section(self.parser.items("sync"), "sync", self.linter_ctx)
            if lint_section_flag:
                self.linter_ctx.passed.append(("general-7", "All general config sections passed cookietemple linting!"))
        else:
            self.linter_ctx.failed.append(("general-7", "Aborted config section linting. Fix missing sections first!"))

    def check_missing_sections(self, parsed_sections) -> bool:
        """
        Examine cookietemple config file for missing sections
        :param parsed_sections: All parsed sections from the user's cookietemple.cfg file
        """
        sections = [
            "bumpversion",
            "bumpversion_files_whitelisted",
            "bumpversion_files_blacklisted",
            "sync_files_blacklisted",
            "sync_level",
            "sync",
        ]
        missing_sections = []
        # for every section check whether it is in the parsed sections or not
        for section in sections:
            if section not in parsed_sections:
                missing_sections.append(section)
        # if there were any missing sections, let linter fail
        if missing_sections:
            miss_section_info = "Cookietemple config file misses section" + "s" if len(missing_sections) > 1 else ""
            self.linter_ctx.failed.append(
                ("general-7", f'{miss_section_info}: {" ".join(section for section in missing_sections)}')
            )
            return False
        else:
            self.linter_ctx.passed.append(("general-7", "All required cookietemple.cfg sections were found!"))
            return True

    def check_section(
        self,
        section_items,
        section_name: str,
        main_linter: TemplateLinter,
        blacklisted_sync_files=None,
        error_code="general-7",
        is_sublinter_calling=False,
    ) -> bool:
        """
        Check requirements 2.) - 5.) stated above.
        :param section_items: A pair (name, value) for all items in a section
        :param section_name: The sections name
        :param main_linter: The linter calling the function
        :param blacklisted_sync_files: The files, that should be blacklisted for sync
        :param error_code: The lint error code, in case of a failing lint function
        :param is_sublinter_calling: Whether the function has been called from a sublinter or not
        """
        # a set containig the section name as a key and its linting rules as values
        # linting rules made of:
        #   1.) a tuple with a variable_name and its value ('*' if value does not care for linting)
        #   => NOTE: if one variable can have multiple valid values, they are separated by '|'
        #
        #   2.) a number, stating the minimum number of items in a section (-1 if number does not care)
        check_set = {
            "bumpversion": [[("current_version", "*")], 1],
            "bumpversion_files_whitelisted": [[("dot_cookietemple", ".cookietemple.yml")], -1],
            "sync_level": [[("ct_sync_level", "patch|minor|major")], 1],
            "sync": [[("sync_enabled", "True|true|Yes|yes|Y|y|False|false|No|no|N|n")], 1],
        }
        if section_name == "sync_files_blacklisted" and is_sublinter_calling:
            return self.apply_section_linting_rules(
                "sync_files_blacklisted", section_items, blacklisted_sync_files, main_linter, error_code
            )

        return self.apply_section_linting_rules(
            section_name, section_items, check_set.get(section_name), main_linter, error_code
        )

    def apply_section_linting_rules(
        self, section: str, section_items, section_lint_rules, main_linter: TemplateLinter, error_code: str
    ) -> bool:
        """
        For each section, check if the applied linting rules are met!
        """
        linting_passed = True
        # if a section needs a concrete number of items, check if this holds true for the section
        if section_lint_rules[1] != -1:
            linting_passed &= len(section_items) == section_lint_rules[1]
        # decide, whether we should check for the whole tuple or just any part of it
        # for each key value pair, that should be blacklisted in the config file sync_blacklisted_files section, check whether it is in the parsed items or not
        for section_tuple in section_lint_rules[0]:
            if section_tuple[1] != "*":
                # it is possible to have several valid values for a concrete section item
                valid_values = section_tuple[1].split("|")
                linting_passed &= any(
                    section_item
                    for idx, section_item in enumerate(section_items)
                    if section_items[idx][0] == section_tuple[0] and section_items[idx][1] in valid_values
                )
            else:
                linting_passed &= any(
                    section_item
                    for idx, section_item in enumerate(section_items)
                    if section_items[idx][0] == section_tuple[0]
                )

        if not linting_passed:
            main_linter.failed.append((error_code, f"Config linting failed for section {section}!"))
        return linting_passed
