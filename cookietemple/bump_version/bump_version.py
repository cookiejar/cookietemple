import click
import re

from configparser import ConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from pathlib import Path
from git import Repo

from cookietemple.create.github_support import is_git_repo


def bump_template_version(new_version: str, pipeline_dir: Path) -> None:
    """
    Update the version number for all files that are whitelisted in the config file.

    INFO on valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
    version formats COOKIETEMPLE allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
    separated by two dots.
    Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
    well as no substring of them will be recognized.

    :param new_version: The new version number that should replace the old one in a cookietemple project
    :param pipeline_dir: The default value is the current working directory, so we´re initially assuming the user
                         bumps the version from the projects top level directory. If this is not the case this parameter
                         shows the path where the projects top level directory is and bumps the version there
    """
    parser = ConfigParser()
    parser.read(f'{pipeline_dir}/cookietemple.cfg')
    current_version = parser.get('bumpversion', 'current_version')
    sections = ['bumpversion_files_whitelisted', 'bumpversion_files_blacklisted']

    # if pipeline_dir was given as handle use cwd since we need it for git add
    ct_cfg_path = f'{str(pipeline_dir)}/cookietemple.cfg' if str(pipeline_dir).startswith(str(Path.cwd())) else \
        f'{str(Path.cwd())}/{pipeline_dir}/cookietemple.cfg'

    # keep path of all files that were changed during bump version
    changed_files = [ct_cfg_path]

    click.echo(click.style(f'Changing version number.\nCurrent version is {current_version}.'
                           f'\nNew version will be {new_version}\n', fg='blue'))

    # for each section (whitelisted and blacklisted files) bump the version (if allowed)
    for section in sections:
        for file, path in parser.items(section):
            not_changed, file_path = replace(f'{pipeline_dir}/{path}', new_version, section)
            # only add file if the version(s) in the file were bumped
            if not not_changed:
                path_changed = file_path if file_path.startswith(str(Path.cwd())) else f'{str(Path.cwd())}/{file_path}'
                changed_files.append(path_changed)

    # update new version in cookietemple.cfg file
    parser.set('bumpversion', 'current_version', new_version)
    with open(f'{pipeline_dir}/cookietemple.cfg', 'w') as configfile:
        parser.write(configfile)

    # check if a project is a git repository and if so, commit bumped version changes
    if is_git_repo(pipeline_dir):
        repo = Repo(pipeline_dir)

        # git add
        click.echo(click.style('Staging template.', fg='blue'))
        repo.git.add(changed_files)

        # git commit
        click.echo(click.style('Committing changes to local git repository.', fg='blue'))
        repo.index.commit(f'Bump version from {current_version} to {new_version}')


def replace(file_path: str, subst: str, section: str) -> (bool, str):
    """
    Replace a version with the new version unless the line is explicitly excluded (marked with
    <<COOKIETEMPLE_NO_BUMP>>).
    Or, in case of blacklisted files, it ignores all lines with version numbers unless they´re explicitly marked
    for bump with tag <<COOKIETEMPLE_FORCE_BUMP>>.

    :param file_path: The path of the file where the version should be updated
    :param subst: The new version that replaces the old one
    :param section: The current section (whitelisted or blacklisted files)

    :return: Whether a file has been changed during bumped and the path of changed file
    """
    # flag that indicates whether no changes were made inside a file
    file_is_unchanged = True
    path_changed = ''

    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # update version if tags were found (and were in the right section)
                if ('<<COOKIETEMPLE_NO_BUMP>>' not in line and not section == 'bumpversion_files_blacklisted') or '<<COOKIETEMPLE_FORCE_BUMP>>' in line:
                    # for info on this regex, see bump_template docstring above
                    tmp = re.sub(r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)', subst, line)
                    new_file.write(tmp)
                    if tmp != line:
                        if file_is_unchanged:
                            click.echo(click.style(f'Updating version number in {file_path}', fg='blue'))
                            file_is_unchanged = False
                            path_changed = file_path
                        click.echo(click.style(
                            f'- {line.strip().replace("<!-- <<COOKIETEMPLE_FORCE_BUMP>> -->", "")}\n', fg='red') + click.style(
                            f'+ {tmp.strip().replace("<!-- <<COOKIETEMPLE_FORCE_BUMP>> -->", "")}', fg='green'))
                        click.echo()
                else:
                    new_file.write(line)
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)

    return file_is_unchanged, path_changed


def can_run_bump_version(new_version: str, project_dir: str) -> bool:
    """
    Ensure that all requirements are met, so that the bump version command can be run successfully.
    This included the following requirements:
    1.) The new version number matches the format like 1.1.0 or 1.1.0-SNAPSHOT required by COOKIETEMPLE versions
    2.) The new version is greater than the current one
    3.) The project is a COOKIETEMPLE project

    :param new_version: The new version
    :param project_dir: The directory of the project
    :return: True if bump version can be run, false otherwise.
    """
    # ensure that the entered version number matches correct format like 1.1.0 or 1.1.0-SNAPSHOT but not 1.2 or 1.2.3.4
    if not re.match(r'(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)', new_version):
        click.echo(click.style('Invalid version specified!\nEnsure your version number has the form '
                               'like 0.0.0 or 15.100.239-SNAPSHOT', fg='red'))
        return False

    # ensure the version is bumped within a project created by Cookietemple
    elif not Path(f'{project_dir}/cookietemple.cfg').is_file():
        click.echo(click.style('Did not found a cookietemple.cfg file. Make sure you are in the right directory '
                               'or specify the path to your projects bump_version.cfg file', fg='red'))
        return False

    # ensure the new version is greater than the current one
    else:
        parser = ConfigParser()
        parser.read(f'{project_dir}/cookietemple.cfg')
        current_version = [int(digit) for digit in parser.get('bumpversion', 'current_version').split('.')]
        new_version = [int(digit) for digit in new_version.split('.')]
        is_greater = False

        if new_version[0] > current_version[0] or new_version[0] == current_version[0] and new_version[1] > current_version[1]:
            is_greater = True
        elif new_version[0] == current_version[0] and new_version[1] == current_version[1] and new_version[2] > current_version[2]:
            is_greater = True

        # the new version is not greater than the current one
        if not is_greater:
            click.echo(click.style(
                f'The new version {".".join(str(n) for n in new_version)} is not greater than the current version {".".join(str(n) for n in current_version)}.'
                f'\nThe new version must be greater than the old one.', fg='red'))

        return is_greater
