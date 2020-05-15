import io
import os
import re

import click
import configparser

from cookietemple.util.dir_util import pf


class TemplateLinter(object):
    """Object to hold linting information and results.
    Attributes:
        files (list): A list of files found during the linting process.
        path (str): Path to the pipeline directory.
        failed (list): A list of tuples of the form: `(<error no>, <reason>)`
        passed (list): A list of tuples of the form: `(<passed no>, <reason>)`
        warned (list): A list of tuples of the form: `(<warned no>, <reason>)`
    """

    def __init__(self, path='.'):
        self.path = path
        self.files = []
        self.pipeline_name = None
        self.passed = []
        self.warned = []
        self.failed = []

    def lint_project(self,
                     calling_class,
                     check_functions: list = None,
                     label: str = 'Running general template tests',
                     custom_check_files: bool = False) -> None:
        """Main linting function.
        Takes the pipeline directory as the primary input and iterates through
        the different linting checks in order. Collects any warnings or errors
        and returns summary at completion. Raises an exception if there is a
        critical error that makes the rest of the tests pointless (eg. no
        pipeline script). Results from this function are printed by the main script.

        :param calling_class: The class that calls the function -> used to get the class methods, which are the linting methods
        :param check_functions: List of functions of the calling class that should be checked. If not set, the default TemplateLinter check functions are called
        :param label: Status message of the current linting method that is about to run
        :param custom_check_files: Set to true if TemplateLinter check_files_exist should not be run
        """
        # Called on its own, so not from a subclass
        if check_functions is None:
            check_functions = ['check_files_exist', 'check_docker', 'check_cookietemple_todos',
                               'check_no_cookiecutter_strings', 'check_version_consistent']
        # Some templates (e.g. latex based) do not adhere to the common programming based templates and therefore do not need to check for e.g. docs
        if custom_check_files:
            check_functions.remove('check_files_exist')

        # Show a progessbar and run all linting functions
        with click.progressbar(check_functions, label=label, item_show_func=repr) as function_names:  # item_show_func=repr leads to some Nones in the bar
            for fun_name in function_names:
                getattr(calling_class, fun_name)()
                if len(self.failed) > 0:
                    click.echo(click.style(f' Found test failures in {fun_name}, halting lint run', fg='red'))
                    break

    def check_files_exist(self):
        """Checks a given pipeline directory for required files.
        Iterates through the pipeline's directory content and checkmarks files
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
            '.coafile',
            '.gitignore',
            '.dependabot/config.yml',
            '.github/ISSUE_TEMPLATE/bug_report.md',
            '.github/ISSUE_TEMPLATE/general_question.md',
            '.github/ISSUE_TEMPLATE/feature_request.md',
            '.github/pull_request.md',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '.travis.yml'
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
            ['.coafile'],
            ['.gitignore'],
            ['.dependabot/config.yml'],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'bug_report.md')],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'feature_request.md')],
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'general_question.md')],
            [os.path.join('.github', 'pull_request_template.md')]
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [

        ]

        files_warn_ifexists = [
            '.travis.yml'
        ]

        # First - critical files. Check that this is actually a COOKIETEMPLE based project
        if not os.path.isfile(pf(self, '.cookietemple.yml')):
            raise AssertionError('.cookietemple.yml not found!! Is this a COOKIETEMPLE project?')

        files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists)

    def check_docker(self):
        """
        Checks that Dockerfile contains the string ``FROM``
        """
        fn = os.path.join(self.path, 'Dockerfile')
        with open(fn, 'r') as fh:
            content = fh.read()

        # Implicitly also checks if empty.
        if 'FROM ' in content:
            self.passed.append((2, click.style('Dockerfile check passed', fg='green')))
            self.dockerfile = [line.strip() for line in content.splitlines()]
            return

        self.failed.append((2, click.style('Dockerfile check failed', fg='red')))

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
                            if len(fname) + len(line) > 70:
                                line = f'{line[:70 - len(fname)]}..'
                            self.warned.append((3, click.style(f'TODO string found in {self._bold_list_items(fname)}: {line}', fg='yellow')))

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
                            if len(fname) + len(line) > 50:
                                line = f'{line[:50 - len(fname)]}..'
                            self.warned.append((4, click.style(f'Cookiecutter string found in \'{fname}\': {line}', fg='yellow')))

    def check_version_consistent(self) -> None:
        """
        This method should check that the version is consistent across all files.
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
        if self.failed.count((5, r'*')) == 0:
            self.passed.append((5, click.style('Versions were consistent over all files', fg='green')))

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
                    line_version = re.search(r'[0-9]+\.[0-9]+\.[0-9]+', line)
                    if line_version:
                        line_version = line_version.group(0)
                        # No match between the current version number and version in source code file
                        if line_version != version:
                            corrected_line = re.sub(r'[0-9]+\.[0-9]+\.[0-9]+', version, line)
                            self.failed.append((5, click.style(f'Version number don´t match in\n {self.path}/{path}:', fg='blue')
                                                + click.style(f'\n {line.strip()} should be {corrected_line.strip()}', fg='red')))

    def print_results(self) -> None:
        """
        Prints the linting results nicely formatted to the console.
        Output is divided into three sections: Passed (green), Warnings (yellow), Failures (red)
        """
        click.echo(f"{click.style('=' * 35, dim=True)}\n          LINTING RESULTS\n{click.style('=' * 35, dim=True)}\n"
                   + click.style('  [{}] {:>4} tests passed\n'.format(u'\u2714', len(self.passed)), fg='green') +
                   click.style('  [!] {:>4} tests had warnings\n'.format(len(self.warned)), fg='yellow') +
                   click.style('  [{}] {:>4} tests failed'.format(u'\u2717', len(self.failed)), fg='red'))

        # Helper function to format test links nicely
        def format_result(test_results):
            """
            Given an error message ID and the message text, return a nicely formatted
            string for the terminal with appropriate ASCII colours.
            """
            print_results = []
            for eid, msg in test_results:
                url = click.style(f'https://cookietemple/linting/errors#{eid}', fg='blue')
                print_results.append(f'{url} : {msg}')
            return '\n  '.join(print_results)

        if len(self.passed) > 0:
            click.echo(click.style(f'Test passed: \n {format_result(self.passed)}', fg='green'))
        if len(self.warned) > 0:
            click.echo(click.style(f'Test Warnings: \n {format_result(self.warned)}', fg='yellow'))
        if len(self.failed) > 0:
            click.echo(click.style(f'Test Failures: \n {format_result(self.failed)}', fg='red'))

    def _bold_list_items(self, files):
        if not isinstance(files, list):
            files = [files]
        bfiles = [click.style(f, bold=True) for f in files]
        return ' or '.join(bfiles)


def files_exist_linting(self, files_fail: list, files_fail_ifexists: list, files_warn: list, files_warn_ifexists: list) -> None:
    """
    Verifies that passed lists of files exist or do not exist.
    Depending on the desired result passing, warning or failing results are appended to the linter object.

    :param self: Linter object
    :param files_fail: list of files which must exist or linting will fail
    :param files_fail_ifexists: list of files which are not allowed to exist or linting will fail
    :param files_warn: list of files which should exist or linting will warn
    :param files_warn_ifexists: list of files which should exist or linting will warn
    """
    # Files that cause an error if they don't exist
    for files in files_fail:
        if any([os.path.isfile(pf(self, f)) for f in files]):
            self.passed.append((1, click.style(f'File found: {self._bold_list_items(files)}', fg='green')))
            self.files.extend(files)
        else:
            self.failed.append((1, click.style(f'File not found: {self._bold_list_items(files)}', fg='red')))

    # Files that cause a warning if they don't exist
    for files in files_warn:
        if any([os.path.isfile(pf(self, f)) for f in files]):
            self.passed.append((1, click.style(f'File found: {self._bold_list_items(files)}', fg='green')))
            self.files.extend(files)
        else:
            self.warned.append((1, click.style(f'File not found: {self._bold_list_items(files)}', fg='yellow')))

    # Files that cause an error if they exist
    for file in files_fail_ifexists:
        if os.path.isfile(pf(self, file)):
            self.failed.append((1, click.style(f'File must be removed: {self._bold_list_items(file)}', fg='red')))
        else:
            self.passed.append((1, click.style(f'File not found check: {self._bold_list_items(file)}', fg='green')))

    # Files that cause a warning if they exist
    for file in files_warn_ifexists:
        if os.path.isfile(pf(self, file)):
            self.warned.append((1, click.style(f'File should be removed: {self._bold_list_items(file)}', fg='yellow')))
        else:
            self.passed.append((1, click.style(f'File not found check: {self._bold_list_items(file)}', fg='green')))
