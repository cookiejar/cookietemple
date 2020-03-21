import os

import click

from cookietemple.util.dir_util import pf


class TemplateLinter(object):
    """Object to hold linting information and results.
    All objects attributes are set, after the :func:`PipelineLint.lint_pipeline` function was called.
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

    def lint_pipeline(self, calling_class, check_functions=None, label: str = 'Running pipeline tests') -> None:
        """Main linting function.
        Takes the pipeline directory as the primary input and iterates through
        the different linting checks in order. Collects any warnings or errors
        and returns summary at completion. Raises an exception if there is a
        critical error that makes the rest of the tests pointless (eg. no
        pipeline script). Results from this function are printed by the main script.

        Raises:
            If a critical problem is found, an ``AssertionError`` is raised.
        """
        # Called on its own, so not from a subclass
        if check_functions is None:
            check_functions = ['check_files_exist', 'check_docker']

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
            '.github/ISSUE_TEMPLATE/feature_request.md',
        Files that *must not* be present::
            none
        Files that *should not* be present::
            '.travis.yml'
        Raises:
            An AssertionError if .cookietemple is not found found.
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
            [os.path.join('.github', 'ISSUE_TEMPLATE', 'feature_request.md')]
        ]

        # List of strings. Fails / warns if any of the strings exist.
        files_fail_ifexists = [

        ]
        files_warn_ifexists = [
            '.travis.yml'
        ]

        # First - critical files. Check that this is actually a COOKIETEMPLE based project
        if not os.path.isfile(pf(self, '.cookietemple')):
            raise AssertionError('.cookietemple not found!! Is this a COOKIETEMPLE project?')

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
            self.passed.append((2, 'Dockerfile check passed'))
            self.dockerfile = [line.strip() for line in content.splitlines()]
            return

        self.failed.append((2, 'Dockerfile check failed'))

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
            self.passed.append((1, f'File found: {self._bold_list_items(files)}'))
            self.files.extend(files)
        else:
            self.failed.append((1, f'File not found: {self._bold_list_items(files)}'))
    # Files that cause a warning if they don't exist
    for files in files_warn:
        if any([os.path.isfile(pf(self, f)) for f in files]):
            self.passed.append((1, f'File found: {self._bold_list_items(files)}'))
            self.files.extend(files)
        else:
            self.warned.append((1, f'File not found: {self._bold_list_items(files)}'))
    # Files that cause an error if they exist
    for file in files_fail_ifexists:
        if os.path.isfile(pf(self, file)):
            self.failed.append((1, f'File must be removed: {self._bold_list_items(file)}'))
        else:
            self.passed.append((1, f'File not found check: {self._bold_list_items(file)}'))
    # Files that cause a warning if they exist
    for file in files_warn_ifexists:
        if os.path.isfile(pf(self, file)):
            self.warned.append((1, f'File should be removed: {self._bold_list_items(file)}'))
        else:
            self.passed.append((1, f'File not found check: {self._bold_list_items(file)}'))
