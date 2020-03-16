import logging

import click
import re

from configparser import SafeConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger('cookietemple bump_version')
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def bump_template_version() -> None:
    """
    This function updates the function for all files that are whitelisted in the config file
    """
    parser = SafeConfigParser()
    parser.read('cookietemple/bump_version/bump_version.cfg')

    new_version = parser.get('bumpversion', 'new_version')

    for file, path in parser.items('bumpversion_files'):
        replace(path,'v[0-9]+.[0-9]+.[0-9]+',str(new_version))


def handle_bump_version_per_file(path: str) -> None:
    """
    This function is a helper function for above. It gets a path as input, reads the file and updates
    the version number unless its marked (blacklisted: <<COOKIETEMPLE_NO_BUMP>>)
    :param path: Path to the file, where version numbers should be updated
    """
    replace(path,'^v[0-9]+.[0-9]+.[0-9]+$')

def replace(file_path, pattern, subst) -> None:
    """
    This
    :param file_path:
    :param pattern:
    :param subst:
    """
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if "<<COOKIETEMPLE_NO_BUMP>>" not in line:
                    tmp = re.sub(pattern, subst, line)
                    new_file.write(tmp)
                else:
                    new_file.write(line)
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
