from pathlib import Path
from click.testing import CliRunner

from cookietemple.cookietemple_cli import create
from cookietemple.util.dir_util import delete_dir_tree
from cookietemple.lint.domains.pub import PubLatexLint


def test_create_pub_thesis_project() -> None:
    """
    Test the creation of a whole pub thesis latex template without GitHub Repo creation!
    """
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(create, input='pub\nthesis\nname\nprojectname\nprojecttitle\nmyuni\nmydep\ndegree\nmyGitHubName\nn')
        project_path = Path('projectname').resolve()
        pub_linter_instance = PubLatexLint(project_path)

        # lint the created project to ensure everything worked fine, but skip common files since its a pub template
        pub_linter_instance.lint_project(pub_linter_instance, label='Test General Linting', custom_check_files=True)

        assert result.exit_code == 0 and matching_project_structure(project_path) and len(pub_linter_instance.failed) == 0
        delete_dir_tree(project_path)


def matching_project_structure(tmp_path: Path) -> bool:
    """
    Iterate over the created directory and check if the project structure is as expected.
    :param tmp_path: Isolated tmp file path for creating our project
    :return: If all files in the project are present and the structure matches
    """
    return set(tmp_path.glob('**/*')) == pub_thesis_contents(tmp_path)


def pub_thesis_contents(tmp_path: Path) -> set:
    """
    Content of a full COOKIETEMPLE thesis latex template
    """
    return {Path(f'{tmp_path}/.cookietemple.yml'), Path(f'{tmp_path}/Figs/University_Crest_Long.eps'),
            Path(f'{tmp_path}/Makefile'), Path(f'{tmp_path}/Figs/CollegeShields/StJohns.eps'),
            Path(f'{tmp_path}/README.rst'), Path(f'{tmp_path}/Chapter2/chapter2.tex'),
            Path(f'{tmp_path}/hooks'), Path(f'{tmp_path}/Chapter2/Figs/Raster/minion.png'),
            Path(f'{tmp_path}/Figs/CollegeShields/src/Kings.svg'), Path(f'{tmp_path}/Acknowledgement'),
            Path(f'{tmp_path}/Figs/CollegeShields/Kings.pdf'),
            Path(f'{tmp_path}/Figs/CollegeShields/src/Trinity.svg'),
            Path(f'{tmp_path}/Figs/CollegeShields/Gonville_and_Caius.jpg'),
            Path(f'{tmp_path}/Figs/University_Crest.pdf'), Path(f'{tmp_path}/Figs/CollegeShields/Kings.eps'),
            Path(f'{tmp_path}/glyphtounicode.tex'), Path(f'{tmp_path}/compile-thesis.sh'),
            Path(f'{tmp_path}/Chapter2/Figs/Vector/TomandJerry.eps'), Path(f'{tmp_path}/Chapter3'),
            Path(f'{tmp_path}/Chapter2/Figs/Vector/WallE.eps'), Path(f'{tmp_path}/Chapter3/chapter3.tex'),
            Path(f'{tmp_path}/Dockerfile'), Path(f'{tmp_path}/Preamble/preamble.tex'),
            Path(f'{tmp_path}/Declaration'), Path(f'{tmp_path}/Figs/CollegeShields/FitzwilliamRed.pdf'),
            Path(f'{tmp_path}/hooks/install.sh'), Path(f'{tmp_path}/Figs/CollegeShields/Queens.eps'),
            Path(f'{tmp_path}/Chapter2/Figs/Vector/minion.eps'), Path(f'{tmp_path}/Appendix1'),
            Path(f'{tmp_path}/Figs/CollegeShields/Queens.pdf'), Path(f'{tmp_path}/Preamble'),
            Path(f'{tmp_path}/Dedication'), Path(f'{tmp_path}/Figs/CollegeShields/src/Downing.svg'),
            Path(f'{tmp_path}/Abstract/abstract.tex'), Path(f'{tmp_path}/Figs/CollegeShields/Peterhouse.pdf'),
            Path(f'{tmp_path}/thesis-info.tex'), Path(f'{tmp_path}/thesis.ps'),
            Path(f'{tmp_path}/Figs/CollegeShields/Fitzwilliam.eps'), Path(f'{tmp_path}/Chapter2/Figs/Raster'),
            Path(f'{tmp_path}/Abstract'), Path(f'{tmp_path}/Figs/CollegeShields/Trinity.pdf'),
            Path(f'{tmp_path}/Figs/CollegeShields/Fitzwilliam.pdf'),
            Path(f'{tmp_path}/Acknowledgement/acknowledgement.tex'),
            Path(f'{tmp_path}/Figs/CollegeShields/StJohns.pdf'),
            Path(f'{tmp_path}/Chapter2/Figs/Raster/TomandJerry.png'), Path(f'{tmp_path}/Chapter1'),
            Path(f'{tmp_path}/Chapter2'), Path(f'{tmp_path}/Figs/CollegeShields/Downing.pdf'),
            Path(f'{tmp_path}/Figs/University_Crest.eps'), Path(f'{tmp_path}/.github'),
            Path(f'{tmp_path}/Variables.ini'), Path(f'{tmp_path}/PhDThesisPSnPDF.cls'),
            Path(f'{tmp_path}/Figs/CollegeShields'), Path(f'{tmp_path}/Figs/CollegeShields/src'),
            Path(f'{tmp_path}/LICENSE'), Path(f'{tmp_path}/Chapter1/chapter1.tex'),
            Path(f'{tmp_path}/Figs/CollegeShields/FitzwilliamRed.eps'),
            Path(f'{tmp_path}/Figs/CollegeShields/Licenses.md'), Path(f'{tmp_path}/References'),
            Path(f'{tmp_path}/.github/workflows/build_thesis.yml'), Path(f'{tmp_path}/Chapter2/Figs'),
            Path(f'{tmp_path}/Appendix1/appendix1.tex'), Path(f'{tmp_path}/Figs/CollegeShields/Downing.eps'),
            Path(f'{tmp_path}/Figs'), Path(f'{tmp_path}/.github/workflows'),
            Path(f'{tmp_path}/sty'), Path(f'{tmp_path}/hooks/pre-commit'),
            Path(f'{tmp_path}/thesis.tex'), Path(f'{tmp_path}/Chapter2/Figs/Raster/WallE.png'),
            Path(f'{tmp_path}/Figs/CollegeShields/src/Queens.svg'),
            Path(f'{tmp_path}/Figs/University_Crest_Long.pdf'), Path(f'{tmp_path}/compile-thesis-windows.bat'),
            Path(f'{tmp_path}/.gitignore'), Path(f'{tmp_path}/sty/breakurl.sty'),
            Path(f'{tmp_path}/thesis.pdf'), Path(f'{tmp_path}/cookietemple.cfg'),
            Path(f'{tmp_path}/References/references.bib'),
            Path(f'{tmp_path}/Figs/CollegeShields/src/Peterhouse.svg'), Path(f'{tmp_path}/Chapter2/Figs/Vector'),
            Path(f'{tmp_path}/Dedication/dedication.tex'), Path(f'{tmp_path}/Figs/CollegeShields/Trinity.eps'),
            Path(f'{tmp_path}/Declaration/declaration.tex')}
