from pathlib import Path
from click.testing import CliRunner

from cookietemple.cookietemple_cli import create
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.lint.domains.web import WebWebsitePythonLint
from tests.create.create_cli.test_cli_template_creation import subdir_dependabot, docs_subdir, subdir_tests


def test_create_basic_web_no_frontend() -> None:
    """
    Test the creation of a basic flask web template with only minimal frontend template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='web\npython\nname\nmail\nprojectname\ndesc\n0.1.1\nMIT\nmyGitHubName\nClick\npytest\nwebsite\nflask\nbasic\nn'
                                             '\ndummy.com\ndummyvm\nn')
        project_path = Path('projectname').resolve()

        web_linter_instance = WebWebsitePythonLint(project_path)

        # lint the created project to ensure everything worked fine
        web_linter_instance.lint_project(web_linter_instance, label='Test General Linting', custom_check_files=False)

        assert result.exit_code == 0 and matching_project_structure(project_path) and len(web_linter_instance.failed) == 0 and \
               set(project_path.iterdir()) == set(basic_dirs(project_path)) and \
               static_assets_no_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/static/assets').glob('**/*')) and \
               basic_template_no_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/templates').glob('**/*'))
        delete_dir_tree(project_path)


def test_create_advanced_web_no_frontend() -> None:
    """
    Test the creation of a advanced flask web template with only minimal frontend template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='web\npython\nname\nmail\nprojectname\ndesc\n0.1.1\nMIT\nmyGitHubName\nClick\npytest\nwebsite\nflask\nadvanced\nn'
                                             '\ndummy.com\ndummyvm\nn')
        project_path = Path('projectname').resolve()
        web_linter_instance = WebWebsitePythonLint(project_path)

        # lint the created project to ensure everything worked fine
        web_linter_instance.lint_project(web_linter_instance, label='Test General Linting', custom_check_files=False)

        assert result.exit_code == 0 and matching_project_structure(project_path) and len(web_linter_instance.failed) == 0 and \
               set(project_path.iterdir()) == set(advanced_dirs(project_path)) and \
               static_assets_no_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/static/assets').glob('**/*')) and \
               advanced_template_no_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/templates').glob('**/*'))
        delete_dir_tree(project_path)


def test_create_basic_web_frontend() -> None:
    """
    Test the creation of a basic flask web template with frontend template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='web\npython\nname\nmail\nprojectname\ndesc\n0.1.1\nMIT\nmyGitHubName\nClick\npytest\nwebsite\nflask\nbasic\ny'
                                             '\nSolidState\ndummy.com\ndummyvm\nn')
        project_path = Path('projectname').resolve()

        web_linter_instance = WebWebsitePythonLint(project_path)

        # lint the created project to ensure everything worked fine
        web_linter_instance.lint_project(web_linter_instance, label='Test General Linting', custom_check_files=False)

        # exit_code 0 indicates the project was linted and passed it
        assert result.exit_code == 0 and matching_project_structure(project_path) and set(project_path.iterdir()) == set(basic_dirs(project_path)) and \
               len(web_linter_instance.failed) == 0 and \
               static_assets_with_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/static/assets').glob('**/*')) and \
               basic_template_with_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/templates').glob('**/*'))
        delete_dir_tree(project_path)


def test_create_advanced_web_frontend() -> None:
    """
    Test the creation of a advanced flask web template with frontend template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='web\npython\nname\nmail\nprojectname\ndesc\n0.1.1\nMIT\nmyGitHubName\nClick\npytest\nwebsite\nflask\nadvanced\nn'
                                             '\ndummy.com\ndummyvm\nn')
        project_path = Path('projectname').resolve()

        web_linter_instance = WebWebsitePythonLint(project_path)

        # lint the created project to ensure everything worked fine
        web_linter_instance.lint_project(web_linter_instance, label='Test General Linting', custom_check_files=False)

        assert result.exit_code == 0 and matching_project_structure(project_path) and set(project_path.iterdir()) == set(advanced_dirs(project_path)) and \
               len(web_linter_instance.failed) == 0 and \
               advanced_template_with_frontend(project_path) == set(Path(f'{str(project_path)}/projectname/templates').glob('**/*'))
        delete_dir_tree(project_path)


def matching_project_structure(tmp_path: Path) -> bool:
    """
    Iterate over the created directory and check if the project structure is as expected.
    :param tmp_path: Isolated tmp file path for creating our project
    :return: If all files in the project are present and the structure matches
    """
    return (set(Path(tmp_path / 'docs').iterdir()) == docs_subdir(tmp_path) and
            (set(Path(tmp_path / 'tests').iterdir()) - {Path(f'{tmp_path}/tests/__pycache__')}) == subdir_tests(tmp_path) and
            set(Path(tmp_path / '.dependabot').iterdir()) == subdir_dependabot(tmp_path))


def basic_dirs(tmp_path) -> set:
    """
    Verify existence of all basic template main directory content
    """
    return {Path(f'{tmp_path}/Makefile'), Path(f'{tmp_path}/requirements_dev.txt'),
            Path(f'{tmp_path}/.dependabot'), Path(f'{tmp_path}/AUTHORS.rst'),
            Path(f'{tmp_path}/.gitignore'), Path(f'{tmp_path}/setup.cfg'),
            Path(f'{tmp_path}/Dockerfile'), Path(f'{tmp_path}/CHANGELOG.rst'),
            Path(f'{tmp_path}/docs'), Path(f'{tmp_path}/tox.ini'),
            Path(f'{tmp_path}/.github'), Path(f'{tmp_path}/.travis.yml'),
            Path(f'{tmp_path}/deployment_scripts'), Path(f'{tmp_path}/README.rst'),
            Path(f'{tmp_path}/.cookietemple.yml'), Path(f'{tmp_path}/requirements.txt'),
            Path(f'{tmp_path}/cookietemple.cfg'), Path(f'{tmp_path}/setup.py'),
            Path(f'{tmp_path}/.editorconfig'), Path(f'{tmp_path}/projectname'),
            Path(f'{tmp_path}/MANIFEST.in'), Path(f'{tmp_path}/.readthedocs.yml'),
            Path(f'{tmp_path}/tests'), Path(f'{tmp_path}/.stylelintrc.json'),
            Path(f'{tmp_path}/CODEOFCONDUCT.rst'), Path(f'{tmp_path}/LICENSE')}


def advanced_dirs(tmp_path) -> set:
    """
    Verify existence of important advanced template main directory content
    """
    return {Path(f'{tmp_path}/babel.cfg')} | basic_dirs(tmp_path)


def basic_template_no_frontend(tmp_path) -> set:
    """
    HTML Templates of the basic template with only minimal frontend
    """
    return {Path(f'{tmp_path}/projectname/templates/errors/500.html'),
            Path(f'{tmp_path}/projectname/templates/errors/410.html'),
            Path(f'{tmp_path}/projectname/templates/errors/error_template.html'),
            Path(f'{tmp_path}/projectname/templates/errors'),
            Path(f'{tmp_path}/projectname/templates/errors/404.html'),
            Path(f'{tmp_path}/projectname/templates/errors/400.html'),
            Path(f'{tmp_path}/projectname/templates/basic_index.html'),
            Path(f'{tmp_path}/projectname/templates/errors/403.html')}


def basic_template_with_frontend(tmp_path) -> set:
    """
    HTML Templates of the basic template with full frontend
    """
    return {Path(f'{tmp_path}/projectname/templates/basic_index_f.html'),
            Path(f'{tmp_path}/projectname/templates/errors/error_template.html'),
            Path(f'{tmp_path}/projectname/templates/errors/404.html'),
            Path(f'{tmp_path}/projectname/templates/errors/400.html'),
            Path(f'{tmp_path}/projectname/templates/errors'),
            Path(f'{tmp_path}/projectname/templates/errors/500.html'),
            Path(f'{tmp_path}/projectname/templates/errors/403.html'),
            Path(f'{tmp_path}/projectname/templates/errors/410.html')}


def advanced_template_no_frontend(tmp_path) -> set:
    """
    HTML Templates of the advanced template with only minimal frontend
    """
    return {Path(f'{tmp_path}/projectname/templates/errors/410.html'),
            Path(f'{tmp_path}/projectname/templates/errors'),
            Path(f'{tmp_path}/projectname/templates/auth/login.html'),
            Path(f'{tmp_path}/projectname/templates/errors/400.html'),
            Path(f'{tmp_path}/projectname/templates/errors/500.html'),
            Path(f'{tmp_path}/projectname/templates/base.html'), Path(f'{tmp_path}/projectname/templates/auth'),
            Path(f'{tmp_path}/projectname/templates/errors/403.html'),
            Path(f'{tmp_path}/projectname/templates/errors/error_template.html'),
            Path(f'{tmp_path}/projectname/templates/auth/register.html'),
            Path(f'{tmp_path}/projectname/templates/index.html'),
            Path(f'{tmp_path}/projectname/templates/errors/404.html')}


def advanced_template_with_frontend(tmp_path) -> set:
    """
    HTML Templates of the advanced template with full frontend
    """
    return {Path(f'{tmp_path}/projectname/templates/errors/410.html'),
            Path(f'{tmp_path}/projectname/templates/errors/404.html'),
            Path(f'{tmp_path}/projectname/templates/auth/login.html'),
            Path(f'{tmp_path}/projectname/templates/base.html'),
            Path(f'{tmp_path}/projectname/templates/errors/error_template.html'),
            Path(f'{tmp_path}/projectname/templates/errors/403.html'),
            Path(f'{tmp_path}/projectname/templates/index.html'),
            Path(f'{tmp_path}/projectname/templates/errors/500.html'),
            Path(f'{tmp_path}/projectname/templates/errors/400.html'),
            Path(f'{tmp_path}/projectname/templates/auth'),
            Path(f'{tmp_path}/projectname/templates/auth/register.html'),
            Path(f'{tmp_path}/projectname/templates/errors')}


def static_assets_no_frontend(tmp_path) -> set:
    """
    Content of static/assets directory with only minimal frontend
    """
    return {Path(f'{tmp_path}/projectname/static/assets/sass/libs'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts'),
            Path(f'{tmp_path}/projectname/static/assets/css/min_css.css'),
            Path(f'{tmp_path}/projectname/static/assets/js/min_jss.js'),
            Path(f'{tmp_path}/projectname/static/assets/css'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/sass'),
            Path(f'{tmp_path}/projectname/static/assets/images/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/js'), Path(f'{tmp_path}/projectname/static/assets/images'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components')}


def static_assets_with_frontend(tmp_path) -> set:
    """
    Content of static/assets directory with full frontend
    """
    return {Path(f'{tmp_path}/projectname/static/assets/sass/components/_table.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_pagination.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_box.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js/jquery.scrollex.min.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_vars.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_actions.scss'),
            Path(f'{tmp_path}/projectname/static/assets/css/fontawesome-all.min.css'),
            Path(f'{tmp_path}/projectname/static/assets/images/bg.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/noscript.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_functions.scss'),
            Path(f'{tmp_path}/projectname/static/assets/css/noscript.css'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/js/min_jss.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_icons.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js/breakpoints.min.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-brands-400.svg'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic08.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-solid-900.svg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_contact.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-regular-400.woff'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-solid-900.eot'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-regular-400.ttf'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic03.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_form.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts'),
            Path(f'{tmp_path}/projectname/static/assets/css/min_css.css'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_vendor.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js/util.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base/_typography.scss'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic06.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_row.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_button.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js/browser.min.js'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-brands-400.eot'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-regular-400.woff2'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic05.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base/_page.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_features.scss'),
            Path(f'{tmp_path}/projectname/static/assets/css/main.css'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/_header.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/_banner.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-brands-400.woff'),
            Path(f'{tmp_path}/projectname/static/assets/css'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_icon.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_image.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_html-grid.scss'),
            Path(f'{tmp_path}/projectname/static/assets/js/jquery.min.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_section.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/main.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-brands-400.ttf'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic02.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_mixins.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-solid-900.woff2'),
            Path(f'{tmp_path}/projectname/static/assets/sass/libs/_breakpoints.scss'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic04.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/components/_list.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-regular-400.svg'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-brands-400.woff2'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic07.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/images/pic01.jpg'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/_wrapper.scss'),
            Path(f'{tmp_path}/projectname/static/assets/images'),
            Path(f'{tmp_path}/projectname/static/assets/images/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/_footer.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-solid-900.woff'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/_menu.scss'),
            Path(f'{tmp_path}/projectname/static/assets/sass/base/_reset.scss'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-solid-900.ttf'),
            Path(f'{tmp_path}/projectname/static/assets/js/main.js'),
            Path(f'{tmp_path}/projectname/static/assets/sass/layout/gitkeep'),
            Path(f'{tmp_path}/projectname/static/assets/webfonts/fa-regular-400.eot')}
