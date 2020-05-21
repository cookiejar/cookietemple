from pathlib import Path
from click.testing import CliRunner

from cookietemple.cookietemple_cli import create
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.lint.domains.cli import CliPythonLint


def test_create_cli_project() -> None:
    """
    Test the creation of a whole python cli template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='cli\npython\nname\nmail\nprojectname\ndesc\n0.1.1\nMIT\nmyGitHubName\npypiname\nClick\npytest\nn')
        project_path = Path('projectname').resolve()
        cli_linter_instance = CliPythonLint(project_path)

        # lint the created project to ensure everything worked fine
        cli_linter_instance.lint_project(cli_linter_instance, custom_check_files=False)

        assert result.exit_code == 0 and matching_project_structure(project_path) and len(cli_linter_instance.failed) == 0
        delete_dir_tree(project_path)


def matching_project_structure(tmp_path: Path) -> bool:
    """
    Iterate over the created directory and check if the project structure is as expected.
    :param tmp_path: Isolated tmp file path for creating our project
    :return: If all files in the project are present and the structure matches
    """
    return (set(tmp_path.iterdir()) == posix_path_super_dir(tmp_path) and set(Path(tmp_path / 'docs').iterdir()) == docs_subdir(tmp_path) and
            (set(Path(tmp_path / 'tests').iterdir()) - {Path(f'{tmp_path}/tests/__pycache__')}) == subdir_tests(tmp_path) and
            set(Path(tmp_path / '.dependabot').iterdir()) == subdir_dependabot(tmp_path) and
            set(Path(tmp_path / '.github').glob('**/*')) == subdir_github(tmp_path) and
            (set(Path(tmp_path / 'projectname').iterdir()) - {Path(f'{tmp_path}/projectname/__pycache__')}) == subdir_maindir(tmp_path))


def docs_subdir(path) -> set:
    return {Path(f'{path}/docs/conf.py'), Path(f'{path}/docs/Makefile'), Path(f'{path}/docs/authors.rst'),
            Path(f'{path}/docs/installation.rst'), Path(f'{path}/docs/make.bat'), Path(f'{path}/docs/index.rst'),
            Path(f'{path}/docs/usage.rst'), Path(f'{path}/docs/changelog.rst'), Path(f'{path}/docs/readme.rst'),
            Path(f'{path}/docs/codeofconduct.rst'), Path(f'{path}/docs/modules.rst'), Path(f'{path}/docs/requirements.txt'),
            Path(f'{path}/docs/_static')}


def subdir_tests(path) -> set:
    return {Path(f'{path}/tests/__init__.py'), Path(f'{path}/tests/test_projectname.py')}


def subdir_maindir(path) -> set:
    return {Path(f'{path}/projectname/__init__.py'), Path(f'{path}/projectname/cli.py'),
            Path(f'{path}/projectname/projectname.py'),
            Path(f'{path}/projectname/files')}


def subdir_dependabot(path) -> set:
    return {Path(f'{path}/.dependabot/config.yml')}


def subdir_github(path) -> set:
    return {Path(f'{path}/.github/pull_request_template.md'), Path(f'{path}/.github/workflows'), Path(f'{path}/.github/ISSUE_TEMPLATE'),
            Path(f'{path}/.github/workflows/build_docs.yml'), Path(f'{path}/.github/workflows/build_package.yml'),
            Path(f'{path}/.github/workflows/flake8_linting.yml'), Path(f'{path}/.github/workflows/pr_to_master_from_dev_only.yml'),
            Path(f'{path}/.github/workflows/publish_package.yml'), Path(f'{path}/.github/workflows/tox_testsuite.yml'),
            Path(f'{path}/.github/ISSUE_TEMPLATE/bug_report.md'), Path(f'{path}/.github/ISSUE_TEMPLATE/feature_request.md'),
            Path(f'{path}/.github/ISSUE_TEMPLATE/general_question.md')}


def posix_path_super_dir(path) -> set:
    return {Path(f'{path}/MANIFEST.in'), Path(f'{path}/.editorconfig'), Path(f'{path}/Makefile'),
            Path(f'{path}/README.rst'), Path(f'{path}/tests'), Path(f'{path}/.readthedocs.yml'), Path(f'{path}/tox.ini'),
            Path(f'{path}/requirements_dev.txt'), Path(f'{path}/.travis.yml'), Path(f'{path}/.gitignore'), Path(f'{path}/projectname'),
            Path(f'{path}/.github'), Path(f'{path}/setup.py'), Path(f'{path}/.cookietemple.yml'), Path(f'{path}/CODEOFCONDUCT.rst'),
            Path(f'{path}/docs'), Path(f'{path}/Dockerfile'), Path(f'{path}/requirements.txt'), Path(f'{path}/setup.cfg'),
            Path(f'{path}/CHANGELOG.rst'), Path(f'{path}/LICENSE'), Path(f'{path}/AUTHORS.rst'),
            Path(f'{path}/.dependabot'), Path(f'{path}/cookietemple.cfg'), Path(f'{path}/.coafile')}
