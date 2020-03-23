import click
import re

from configparser import SafeConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

from pathlib import Path


def bump_template_version(new_version: str, pipeline_dir: Path) -> None:
    """
    This function updates the function for all files that are whitelisted in the config file
    :param new_version: The new version number that should replace the old one in a cookietemple project
    :param pipeline_dir: The default value is the current working directory, so we´re initially assuming the user
                         bumps the version from the projects top level directory. If this is not the case this parameter
                         shows the path where the projects top level directory is and bumps the version there
    """

    parser = SafeConfigParser()
    parser.read(f'{pipeline_dir}/bump_version.cfg')
    current_version = parser.get('bumpversion', 'current_version')

    click.echo(click.style(f'Changing version number.\nCurrent version is {current_version}.'
                           f'\nNew version will be {new_version}\n', fg='blue'))

    for file, path in parser.items('bumpversion_files'):
        replace(path, new_version)

    parser.set('bumpversion', 'current_version', new_version)
    with open(f'{pipeline_dir}/bump_version.cfg', 'w') as configfile:
        parser.write(configfile)


def replace(file_path: str, subst: str) -> None:
    """
    This function actually replaces a version with the new version unless its blacklisted (marked with
    <<COOKIETEMPLE_NO_BUMP>>)!
    :param file_path: The path of the file where the version should be updated
    :param subst: The new version that replaces the old one
    """
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            click.echo(click.style(f'Updating version number in {file_path}', fg='blue'))
            for line in old_file:
                if "<<COOKIETEMPLE_NO_BUMP>>" not in line:
                    tmp = re.sub(r"[0-9]+.[0-9]+.[0-9]+", subst, line)
                    new_file.write(tmp)
                    if tmp != line:
                        click.echo(click.style(
                            f'- {line}', fg='red') + click.style(
                            f'+ {tmp}', fg='green'))
                else:
                    new_file.write(line)
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
