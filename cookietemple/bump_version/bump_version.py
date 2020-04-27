import click
import re

from configparser import ConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from pathlib import Path


def bump_template_version(new_version: str, pipeline_dir: Path) -> None:
    """
    Update the version number for all files that are whitelisted in the config file
    :param new_version: The new version number that should replace the old one in a cookietemple project
    :param pipeline_dir: The default value is the current working directory, so we´re initially assuming the user
                         bumps the version from the projects top level directory. If this is not the case this parameter
                         shows the path where the projects top level directory is and bumps the version there
    """
    parser = ConfigParser()
    parser.read(f'{pipeline_dir}/cookietemple.cfg')
    current_version = parser.get('bumpversion', 'current_version')
    sections = ['bumpversion_files_whitelisted', 'bumpversion_files_blacklisted']

    click.echo(click.style(f'Changing version number.\nCurrent version is {current_version}.'
                           f'\nNew version will be {new_version}\n', fg='blue'))

    # for each section (whitelisted and blacklisted files) bump the version (if allowed)
    for section in sections:
        for file, path in parser.items(section):
            replace(f'{pipeline_dir}/{path}', new_version, section)

    # update new version in cookietemple.cfg file
    parser.set('bumpversion', 'current_version', new_version)
    with open(f'{pipeline_dir}/cookietemple.cfg', 'w') as configfile:
        parser.write(configfile)


def replace(file_path: str, subst: str, section: str) -> None:
    """
    Replace a version with the new version unless the line is explicitly excluded (marked with
    <<COOKIETEMPLE_NO_BUMP>>).
    Or, in case of blacklisted files, it ignores all lines with version numbers unless they´re explicitly marked
    for bump with tag <<COOKIETEMPLE_FORCE_BUMP>>.

    :param file_path: The path of the file where the version should be updated
    :param subst: The new version that replaces the old one
    :param section: The current section (whitelisted or blacklisted files)
    """
    # flag that indicates whether no changes were made inside a file
    file_is_unchanged = True

    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # update version if tags were found (and were in the right section)
                if ('<<COOKIETEMPLE_NO_BUMP>>' not in line and not section == 'bumpversion_files_blacklisted') or '<<COOKIETEMPLE_FORCE_BUMP>>' in line:
                    tmp = re.sub(r'[0-9]+\.[0-9]+\.[0-9]+', subst, line)
                    new_file.write(tmp)
                    if tmp != line:
                        if file_is_unchanged:
                            click.echo(click.style(f'Updating version number in {file_path}', fg='blue'))
                            file_is_unchanged = False
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


def can_do_bump_version(new_version: str, project_dir: str) -> bool:
    """
    Ensure that all requirements are met, so that the bump version command can be run successfully.
    This included the following requirements:
    1.) A new version is specified
    2.) The new version matches the format [0-9]+.[0-9]+.[0-9]+
    3.) The new version is greater than the current one
    4.) The project is a Cookietemple project

    :param new_version: The new version
    :param project_dir: The directory of the project
    :return: True if bump version can be run, false otherwise.
    """
    # print error message if no new version was specified
    if not new_version:
        click.echo(click.style('No new version specified.\nPlease specify a new version using '
                               '\'cookietemple bump_version my.new.version\'', fg='red'))
        return False

    # ensure that the entered version number matches correct format
    elif not re.match(r"[0-9]+\.[0-9]+\.[0-9]+", new_version):
        click.echo(click.style('Invalid version specified!\nEnsure your version number has the form '
                               'like 0.0.0 or 15.100.239', fg='red'))
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
        current_version = parser.get('bumpversion', 'current_version').split('.')
        new_version = new_version.split('.')
        is_greater = False

        if new_version[0] > current_version[0] or new_version[0] == current_version[0] and new_version[1] > current_version[1]:
            is_greater = True
        elif new_version[0] == current_version[0] and new_version[1] == current_version[1] and new_version[2] > current_version[2]:
            is_greater = True

        # the new version is not greater than the current one
        if not is_greater:
            click.echo(click.style(
                f'The new version {".".join(n for n in new_version)} is not greater than the current version {".".join(n for n in current_version)}.'
                f'\nThe new version must be greater than the old one.', fg='red'))

        return is_greater
