import io
import os
import re
import configparser
import sys

import rich.progress
import rich.markdown
import rich.panel
import rich.console

from packaging import version
from itertools import groupby

from cookietemple.util.dir_util import pf


class TemplateLinter(object):
    """Object to hold linting information and results.
    Attributes:
        files (list): A list of files found during the linting process.
        path (str): Path to the project directory.
        failed (list): A list of tuples of the form: `(<error no>, <reason>)`
        passed (list): A list of tuples of the form: `(<passed no>, <reason>)`
        warned (list): A list of tuples of the form: `(<warned no>, <reason>)`
    """

    def __init__(self, path='.'):
        self.path = path
        self.files = []
        self.passed = []
        self.warned = []
        self.failed = []

    def lint_project(self, calling_class, check_functions: list = None, custom_check_files: bool = False, is_subclass_calling=True) -> None:
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
            check_functions = [func for func in dir(TemplateLinter) if (callable(getattr(TemplateLinter, func)) and not func.startswith('_'))]
            # Remove internal functions
            check_functions = list(set(check_functions).difference({'lint_project', 'print_results', 'check_version_match'}))
        # Some templates (e.g. latex based) do not adhere to the common programming based templates and therefore do not need to check for e.g. docs
        # or lint changelog
        if custom_check_files:
            check_functions.remove('check_files_exist')
            check_functions.remove('lint_changelog')

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
                progress.update(lint_progress, advance=1, func_name=fun_name)
                if fun_name == 'check_files_exist':
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
            'CHANGELOG.rst'
            '[LICENSE, LICENSE.md, LICENCE, LICENCE.md]'
            'docs/index.rst'
            'docs/readme.rst'
            'docs/changelog.rst'
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
            ['Dockerfile'],
            ['cookietemple.cfg'],
            ['Makefile'],
            ['README.rst'],
            ['CHANGELOG.rst'],
            ['LICENSE', 'LICENSE.md', 'LICENCE', 'LICENCE.md'],  # NB: British / American spelling
            [os.path.join('docs', 'index.rst')],
            [os.path.join('docs', 'readme.rst')],
            [os.path.join('docs', 'changelog.rst')],
            [os.path.join('docs', 'installation.rst')],
            [os.path.join('docs', 'usage.rst')],
        ]

        files_warn = [
            ['.gitignore'],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'bug_report.md')],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'feature_request.md')],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'general_question.md')],
            [os.path.join('.github', 'pull_request_template.md')]
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [

        ]

        files_warn_ifexists = [

        ]

        # First - critical files. Check that this is actually a cookietemple based project
        if not os.path.isfile(pf(self, '.cookietemple.yml')):
            print('[bold red] .cookietemple.yml not found! Is this a cookietemple project?')
            sys.exit(1)

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists, is_subclass_calling)

    def lint_changelog(self):
        """
        Lint the Changelog.rst file
        """
        changelog_path = os.path.join(self.path, 'CHANGELOG.rst')
        linter = ChangelogLinter(changelog_path, self)
        if not len(linter.changelog_content) < 3:
            # lint header first
            header_lint_code, header_detected, header_lint_passed = linter.lint_header()
            if header_lint_code != -1 and header_detected:
                # if head linting did not found any errors lint sections
                section_lint_passed = linter.lint_changelog_section()
                if section_lint_passed and header_lint_passed:
                    self.passed.append(('general-6', 'Changelog linting passed!'))
            elif not header_detected:
                self.failed.append(('general-6', 'Changelog does not seem to contain a header or your header syntax is wrong!'))
        else:
            self.failed.append(('general-6', 'Changelog does not seem to contain a header and/or at least one section!'))

    def check_docker(self):
        """
        Checks that Dockerfile contains the string ``FROM``
        """
        fn = os.path.join(self.path, 'Dockerfile')
        with open(fn, 'r') as fh:
            content = fh.read()

        # Implicitly also checks if empty.
        if 'FROM ' in content:
            self.passed.append(('general-2', 'Dockerfile check passed'))
            self.dockerfile = [line.strip() for line in content.splitlines()]
            return

        self.failed.append((2, 'Dockerfile check failed'))

    def check_cookietemple_todos(self) -> None:
        """
        Go through all template files looking for the string 'TODO COOKIETEMPLE:'
        """
        ignore = ['.git']
        if os.path.isfile(os.path.join(self.path, '.gitignore')):
            with io.open(os.path.join(self.path, '.gitignore'), 'rt', encoding='latin1') as file:
                for line in file:
                    ignore.append(os.path.basename(line.strip().rstrip('/')))
        for root, dirs, files in os.walk(self.path):
            # Ignore files
            for ignore_file in ignore:
                if ignore_file in dirs:
                    dirs.remove(ignore_file)
                if ignore_file in files:
                    files.remove(ignore_file)
            for fname in files:
                with io.open(os.path.join(root, fname), 'rt', encoding='latin1') as file:
                    for line in file:
                        if 'TODO COOKIETEMPLE:' in line:
                            line = line.replace('<!--', '') \
                                .replace('-->', '') \
                                .replace('# TODO COOKIETEMPLE: ', '') \
                                .replace('// TODO COOKIETEMPLE: ', '') \
                                .replace('TODO COOKIETEMPLE: ', '').strip()
                            self.warned.append(('general-3', f'TODO string found in {self._wrap_quotes(fname)}: {line}'))

    def check_no_cookiecutter_strings(self) -> None:
        """
        Verifies that no cookiecutter strings are in any of the files
        """

        for root, dirs, files in os.walk(self.path):
            for fname in files:
                with io.open(os.path.join(root, fname), 'rt', encoding='latin1') as file:
                    for line in file:
                        # TODO We should also add some of the more advanced cookiecutter if statements, raw statements etc
                        regex = re.compile('{{ cookiecutter.* }}')
                        if regex.match(line):
                            line = f'{line[:50 - len(fname)]}..'
                            self.warned.append(('general-4', f'Cookiecutter string found in \'{fname}\': {line}'))

    def check_version_consistent(self) -> None:
        """
        This method verifies that the project version is consistent across all files.
        """
        parser = configparser.ConfigParser()
        parser.read(f'{self.path}/cookietemple.cfg')
        sections = ['bumpversion_files_whitelisted', 'bumpversion_files_blacklisted']

        current_version = parser.get('bumpversion', 'current_version')

        cwd = os.getcwd()
        os.chdir(self.path)

        # check if the version matches current version in each listed file (depending on whitelisted or blacklisted)
        for section in sections:
            for file, path in parser.items(section):
                self.check_version_match(path, current_version, section)
        os.chdir(cwd)
        # Pass message if there weren't any inconsistencies within the version numbers
        if not any('general-5' in tup[0] for tup in self.failed):
            self.passed.append(('general-5', 'Versions were consistent over all files'))

    def check_version_match(self, path: str, version: str, section: str) -> None:
        """
        Check if the versions in a file are consistent with the current version in the cookietemple.cfg
        :param path: The current file-path to check
        :param version: The current version of the project specified in the cookietemple.cfg file
        :param section: The current section (blacklisted or whitelisted files)
        """
        with open(path) as file:
            for line in file:
                # if a tag is found and (depending on wether its a white or blacklisted file) check if the versions are matching
                if ('<<COOKIETEMPLE_NO_BUMP>>' not in line and not section == 'bumpversion_files_blacklisted') or '<<COOKIETEMPLE_FORCE_BUMP>>' in line:
                    line_version = re.search(r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)', line)
                    if line_version:
                        line_version = line_version.group(0)
                        # No match between the current version number and version in source code file
                        if line_version != version:
                            corrected_line = re.sub(r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)', version, line)
                            self.failed.append(('general-5', f'Version number don´t match in\n {path}: \n {line.strip()} should be {corrected_line.strip()}'))

    def print_results(self):
        console = rich.console.Console()
        console.print()
        console.rule("[bold green] LINT RESULTS")
        console.print()
        console.print(
            f'     [bold green][[\u2714]] {len(self.passed):>4} tests passed\n     [bold yellow][[!]] {len(self.warned):>4} tests had warnings\n'
            f'     [bold red][[\u2717]] {len(self.failed):>4} tests failed',
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
                results.append(f"1. [https://cookietemple/linting/errors#{eid}](https://cookietemple/linting/errors#{eid}): {msg}")
            return rich.markdown.Markdown("\n".join(results))

        if len(self.passed) > 0:
            console.print()
            console.rule("[bold green][[\u2714]] Tests Passed", style="green")
            console.print(rich.panel.Panel(format_result(self.passed), style="green"), no_wrap=True, overflow="ellipsis")
        if len(self.warned) > 0:
            console.print()
            console.rule("[bold yellow][[!]] Test Warnings", style="yellow")
            console.print(rich.panel.Panel(format_result(self.warned), style="yellow"), no_wrap=True, overflow="ellipsis")
        if len(self.failed) > 0:
            console.print()
            console.rule("[bold red][[\u2717]] Test Failures", style="red")
            console.print(rich.panel.Panel(format_result(self.failed), style="red"), no_wrap=True, overflow="ellipsis")

    def _wrap_quotes(self, files):
        if not isinstance(files, list):
            files = [files]
        bfiles = [f"`{file}`" for file in files]

        return " or ".join(bfiles)

    def _strip_ansi_codes(self, string, replace_with=""):
        # https://stackoverflow.com/a/14693789/713980
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

        return ansi_escape.sub(replace_with, string)


def files_exist_linting(self,
                        files_fail: list,
                        files_fail_ifexists: list,
                        files_warn: list,
                        files_warn_ifexists: list,
                        is_subclass_calling=True,
                        handle: str = 'general') -> None:
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
            self.failed.append(('{handle}-1', f'File not found: {self._wrap_quotes(files)}'))
    # flag that indiactes whether all required files exist or not
    if all_exists:
        # called linting from a specific template linter
        if is_subclass_calling:
            self.passed.append((f'{handle}-1', f'All required {handle} specific files were found!'))
        # called as general linting
        else:
            self.passed.append((f'{handle}-1', f'All required {handle} files were found!'))

    # Files that cause a warning if they don't exist
    for files in files_warn:
        if any([os.path.isfile(pf(self, f)) for f in files]):
            # pass cause if a file was found it will be summarised in one "all required files found" statement
            pass
        else:
            self.warned.append((f'{handle}-1', f'File not found: {self._wrap_quotes(files)}'))

    # Files that cause an error if they exist
    for file in files_fail_ifexists:
        if os.path.isfile(pf(self, file)):
            self.failed.append((f'{handle}-1', f'File must be removed: {self._wrap_quotes(file)}'))
        else:
            self.passed.append((f'{handle}-1', f'File not found check: {self._wrap_quotes(file)}'))

    # Files that cause a warning if they exist
    for file in files_warn_ifexists:
        if os.path.isfile(pf(self, file)):
            self.warned.append((f'{handle}-1', f'File should be removed: {self._wrap_quotes(file)}'))
        else:
            self.passed.append((f'{handle}-1', f'File not found check: {self._wrap_quotes(file)}'))


class GetLintingFunctionsMeta(type):
    def get_linting_functions(cls):
        """
        Fetches all specific linting methods and returns them as a list.
        Used for all template specific linters

        :param cls: The specific linting class
        """
        specific_linter_function_names = ([func for func in dir(cls) if (callable(getattr(cls, func)) and not func.startswith('__'))])
        general_linter_function_names = ([func for func in dir(TemplateLinter) if (callable(getattr(TemplateLinter, func)) and not func.startswith('__'))])
        cls_only_funcs = list(set(specific_linter_function_names) - set(general_linter_function_names))
        cls_only_funcs.remove('lint')  # remove 'lint', since we only want the newly defined methods and not the method itself

        return cls_only_funcs

    def __call__(self, *args, **kwargs):
        # create the new class as normal
        cls = type.__call__(self, *args)

        # set the methods attribute to a list of all specific linting functions
        setattr(cls, "methods", self.get_linting_functions())

        return cls


class ChangelogLinter:
    """
    A linter for our templates Changelog.rst to ensure consistency across templates

    :attribute self.changelog_path: Path to the changelog file
    :attribute self.main_linter: The calling linter
    :attribute self.changelog_content: The content line by line of the CHANGELOG.rst file
    :attribute self.line_counter: A counter to keep track of the currents line index
    :attribute self.header_offset: An offset value to indicate where the CHANGELOG header ends
    """

    def __init__(self, path, linter: TemplateLinter):
        """
        :param path: Path to the Changelog file
        :param linter: a reference to the calling linter
        """
        self.changelog_path = path
        self.main_linter = linter
        self.changelog_content = self.init_changelog_lint_content()
        self.line_counter = 0
        self.header_offset = 0

    def lint_header(self) -> (int, bool, bool):
        """
        Lint the header which consists of an optional label, the headline CHANGELOG and an optional small description
        """
        header_detected = False
        for line in self.changelog_content:
            # lint the header until we found a section header
            if self.match_section_header(line):
                if self.changelog_content[self.line_counter + 1] >= f'{"-" * (len(line) - 1)}\n':
                    return self.header_offset, header_detected, True
                else:
                    """
                    This also helps with bump-version and automatic section adding to ensure a correct section start.
                    Example:
                    1.2.3 (12.12.2020)
                    Some text were underscores belong for correct underline
                    """
                    self.main_linter.failed.append(('general-6', 'Invalid section header start detected!'))
                    return -1, header_detected, False
            # lint header (optional label, title and an optional small description)
            elif any(cl in line for cl in ['CHANGELOG', 'Changelog']):
                head_liner = f'{"=" * len(line)}\n'
                header_ok = self.changelog_content[self.line_counter - 1] == head_liner and self.changelog_content[self.line_counter + 1] == head_liner
                """
                Example:
                ======
                MY HEADER IS TOO LONG
                =====================
                """
                if not header_ok:
                    self.main_linter.failed.append(('general-6', 'Your Changelog header syntax does not match length of your Changelogs title!'))
                    return -1, header_detected, False
                header_detected = True

            if self.header_offset >= len(self.changelog_content) - 2:
                """
                A Changelog EVER should contain at least one section (thus when the template has been created)!
                Example
                .. changelog_f

                =========
                CHANGELOG
                =========

                End
                """
                self.main_linter.failed.append(('general-6', 'No changelog sections detected!'))
                return -1, header_detected, False
            self.header_offset += 1
            self.line_counter += 1

    def lint_changelog_section(self) -> bool:
        """
        Lint a changelog section
        Example:
        1.2.3 (2020-12-06)
        ------------------
        **Added**
        We added ...

        **Fixed**
        We fixed ...

        **Dependencies**
        Dependencies ...

        **Deprecated**
        Whats deprecated now ...
        """
        # this will actually not generate a copy of the list, it just copies a reference
        section_changelog_content = self.changelog_content[self.header_offset:]
        versions = []

        # define separator keys
        def split_condition(x):
            is_split_key = self.match_section_header(x)
            # keep track of the versions
            if is_split_key:
                versions.append(x)
            return is_split_key

        grouper = groupby(section_changelog_content, key=split_condition)
        sections = list((list(sect) for split, sect in grouper if not split))

        # keep track how many sections seen so far
        section_nr = 0
        # keep track of the last version of the processed section; init with high number
        last_version = '1000000.1000000.1000000'

        for section in sections:
            # check if newer sections have a strict greater version than older sections
            current_section_version = versions[section_nr][:-1].replace('-SNAPSHOT', '').split(' ')[0]
            if version.parse(current_section_version) >= version.parse(last_version):
                self.main_linter.failed.append(('general-6', 'Older sections cannot have greater version numbers than newer sections!'))
                return False
            else:
                last_version = current_section_version

            # check if ever section subheader is underlined correctly
            if not section[0] >= f'{"-" * (len(versions[section_nr]) - 1)}\n':
                self.main_linter.failed.append(('general-6', 'Your sections subheader underline does not match the headers length!'))
                return False
            try:
                index_order_ok = section.index('**Added**\n') < section.index('**Fixed**\n') < section.index('**Dependencies**\n') < \
                                 section.index('**Deprecated**\n')
                if not index_order_ok:
                    """
                    Example (for a section)
                    1.2.3 (2020-12-06)
                    **Added**

                    **Fixed**

                    **Deprecated

                    **Dependencies**

                    Dependencies and Deprecated should be changed
                    """
                    self.main_linter.failed.append(('general-6', 'Sections subheader order should be **Added**\n**Fixed**\n'
                                                                 '**Dependencies**\n**Deprecated**!'))
                    return False

            except ValueError:
                """
                Example when missing a subsection
                1.2.3 (2020-12-06)
                **Added**

                **Deprecated

                **Dependencies**

                Fixed section is missing
                """
                self.main_linter.failed.append(('general-6', 'Section misses one or more required subsections!'))
                return False
            section_nr += 1
        return True

    def match_section_header(self, line: str) -> bool:
        """
        Check if beginning of a section header was reached
        :param line: The current line that has been read
        """
        no_snapshot_header = re.compile(r'^(?<!\.)\d+(?:\.\d+){2}(?!\.) \(\d\d\d\d-\d\d-\d\d\)$')
        snapshot_header = re.compile(r'^(?<!\.)\d+(?:\.\d+){2}(?!\.)-SNAPSHOT \(\d\d\d\d-\d\d-\d\d\)$')

        return bool(no_snapshot_header.match(line)) or bool(snapshot_header.match(line))

    def init_changelog_lint_content(self) -> list:
        """
        Reads from the project's CHANGELOG.rst.
        :return: Changelog.rst contents line by line as a list
        """
        with open(self.changelog_path, 'r') as f:
            content = f.readlines()

        return content
