import pytest
import os

from cookietemple.lint.template_linter import TemplateLinter
from cookietemple.lint.domains.cli import CliPythonLint
from cookietemple.lint.domains.web import WebWebsitePythonLint
from cookietemple.lint.domains.pub import PubLatexLint


@pytest.fixture
def get_template_linter():
    """
    List of all template linters
    """
    return [CliPythonLint, WebWebsitePythonLint, PubLatexLint]


def test_lint_good_example(capfd, get_template_linter) -> None:
    """
    Test single linting function like _todo string or raw cookiecutter statement detection and version consistency checking
    in a clean example with no fails.
    """
    for linter in get_template_linter:
        test_linter: TemplateLinter = linter(str(os.path.abspath(os.path.dirname(__file__))) + '/lint_test_files/lint_good_file')

        # check for each linter if it recognizes the bad examples
        test_linter.check_cookietemple_todos()
        test_linter.check_no_cookiecutter_strings()
        test_linter.check_version_match(f'{test_linter.path}/lint_good_test_file', '1.0.0-SNAPSHOT', 'bumpversion_files_whitelisted')

        test_linter.print_results()

        out, err = capfd.readouterr()

        assert len(test_linter.warned) == 0 and len(test_linter.failed) == 0


def test_lint_bad_example(capfd, get_template_linter) -> None:
    """
    Test single linting function like _todo string or raw cookiecutter statement detection and version consistency checking
    in a bad example with some violations.
    """
    for linter in get_template_linter:
        test_linter: TemplateLinter = linter(str(os.path.abspath(os.path.dirname(__file__))) + '/lint_test_files')

        # check for each linter if it recognizes the bad examples
        test_linter.check_cookietemple_todos()
        test_linter.check_no_cookiecutter_strings()
        test_linter.check_version_match(f'{test_linter.path}/lint_bad_test_file', '1.0.0', 'bumpversion_files_whitelisted')
        test_linter.print_results()

        assert len(test_linter.warned) == 1 and len(test_linter.failed) == 1
