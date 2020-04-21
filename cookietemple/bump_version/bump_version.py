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
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            click.echo(click.style(f'Updating version number in {file_path}', fg='blue'))
            for line in old_file:
                # update version if tags were found (and were in the right section)
                if ('<<COOKIETEMPLE_NO_BUMP>>' not in line and not section == 'bumpversion_files_blacklisted') or '<<COOKIETEMPLE_FORCE_BUMP>>' in line:
                    tmp = re.sub(r'[0-9]+\.[0-9]+\.[0-9]+', subst, line)
                    new_file.write(tmp)
                    if tmp != line:
                        click.echo(click.style(
                            f'- {line.strip()}\n', fg='red') + click.style(
                            f'+ {tmp.strip()}', fg='green'))
                        click.echo()
                else:
                    new_file.write(line)
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
