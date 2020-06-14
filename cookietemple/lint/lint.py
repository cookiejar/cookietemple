import sys
from pathlib import Path
import click
from ruamel.yaml import YAML

from cookietemple.lint.template_linter import TemplateLinter
from cookietemple.lint.domains.cli import CliPythonLint, CliJavaLint
from cookietemple.lint.domains.web import WebWebsitePythonLint
from cookietemple.lint.domains.gui import GuiJavaLint
from cookietemple.lint.domains.pub import PubLatexLint


def lint_project(project_dir: str, is_create: bool = False) -> TemplateLinter:
    """
    Verifies the integrity of a project to best coding and practices.
    Runs a set of general linting functions, which all templates share and afterwards runs template specific linting functions.
    All results are collected and presented to the user.
    """
    # Detect which template the project is based on
    template_handle = get_template_handle(project_dir)

    switcher = {
        'cli-python': CliPythonLint,
        'cli-java': CliJavaLint,
        'web-website-python': WebWebsitePythonLint,
        'gui-java': GuiJavaLint,
        'pub-thesis-latex': PubLatexLint
    }

    try:
        lint_obj = switcher.get(template_handle)(project_dir)
    except TypeError:
        click.echo(click.style(f'Unable to find linter for handle {template_handle}! Aborting...', fg='red'))
        sys.exit(1)
        
    # Run the linting tests
    try:
        # Disable check files?
        disable_check_files_templates = ['pub-thesis-latex']
        if template_handle in disable_check_files_templates:
            disable_check_files = True
        else:
            disable_check_files = False
        # Run non project specific linting
        click.echo(click.style('Running general linting', fg='blue'))
        lint_obj.lint_project(super(lint_obj.__class__, lint_obj), custom_check_files=disable_check_files, is_subclass_calling=False)

        # Run the project specific linting
        click.echo(click.style(f'Running {template_handle} linting', fg='blue'))

        # for every python project that is created autopep8 will run one time
        # when linting en existing python COOKIETEMPLE project, autopep8 should be now optional,
        # because (for example) it messes up Jinja syntax (if included in project)
        if 'python' in template_handle:
            lint_obj.lint(is_create)
        else:
            lint_obj.lint()
    except AssertionError as e:
        click.echo(click.style(f'Critical error: {e}', fg='red'))
        click.echo(click.style('Stopping tests...', fg='red'))
        return lint_obj

    # Print the results
    lint_obj.print_results()

    # Exit code
    if len(lint_obj.failed) > 0:
        click.echo(click.style('Sorry, some tests failed - exiting with a non-zero error code...\n'))


def get_template_handle(dot_cookietemple_path: str = '.cookietemple.yml') -> str:
    """
    Reads the .cookietemple file and extracts the template handle
    :param dot_cookietemple_path: path to the .cookietemple file
    :return: found template handle
    """
    path = Path(f'{dot_cookietemple_path}/.cookietemple.yml')
    if not path.exists():
        click.echo(click.style('.cookietemple.yml not found. Is this a COOKIETEMPLE project?', fg='red'))
        sys.exit(1)
    yaml = YAML(typ='safe')
    dot_cookietemple_content = yaml.load(path)

    return dot_cookietemple_content['template_handle']
