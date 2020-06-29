import os
import sys
import click
import re
from packaging import version
from configparser import ConfigParser
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
from pathlib import Path
from git import Repo
from datetime import datetime

from cookietemple.create.github_support import is_git_repo
from cookietemple.lint.template_linter import TemplateLinter


class VersionBumper:
    """
    Responsible for bumping the version across a cookietemple project
    """

    def __init__(self, project_dir, downgrade):
        self.parser = ConfigParser()
        self.parser.read(f'{project_dir}/cookietemple.cfg')
        self.CURRENT_VERSION = self.parser.get('bumpversion', 'current_version')
        self.downgrade_mode = downgrade
        self.top_level_dir = project_dir

    def bump_template_version(self, new_version: str, project_dir: Path) -> None:
        """
        Update the version number for all files that are whitelisted in the config file.

        INFO on valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
        version formats cookietemple allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
        separated by two dots.
        Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
        well as no substring of them will be recognized.

        :param new_version: The new version number that should replace the old one in a cookietemple project
        :param project_dir: The default value is the current working directory, so we´re initially assuming the user
                             bumps the version from the projects top level directory. If this is not the case this parameter
                             shows the path where the projects top level directory is and bumps the version there
        """
        sections = ['bumpversion_files_whitelisted', 'bumpversion_files_blacklisted']

        # if project_dir was given as handle use cwd since we need it for git add
        ct_cfg_path = f'{str(project_dir)}/cookietemple.cfg' if str(project_dir).startswith(str(Path.cwd())) else \
            f'{str(Path.cwd())}/{project_dir}/cookietemple.cfg'
        # path to CHANGELOG.rst file
        changelog_path = f'{str(project_dir)}/CHANGELOG.rst' if str(project_dir).startswith(str(Path.cwd())) else \
            f'{str(Path.cwd())}/{project_dir}/CHANGELOG.rst'

        # keep path of all files that were changed during bump version
        changed_files = [ct_cfg_path, changelog_path]

        click.echo(click.style(f'Changing version number.\nCurrent version is {self.CURRENT_VERSION}.'
                               f'\nNew version will be {new_version}\n', fg='blue'))

        # for each section (whitelisted and blacklisted files) bump the version (if allowed)
        for section in sections:
            for file, path in self.parser.items(section):
                not_changed, file_path = self.replace(f'{project_dir}/{path}', new_version, section)
                # only add file if the version(s) in the file were bumped
                if not not_changed:
                    path_changed = file_path if file_path.startswith(str(Path.cwd())) else f'{str(Path.cwd())}/{file_path}'
                    changed_files.append(path_changed)

        # update new version in cookietemple.cfg file
        self.parser.set('bumpversion', 'current_version', new_version)
        with open(f'{project_dir}/cookietemple.cfg', 'w') as configfile:
            self.parser.write(configfile)

        # add a new changelog section when downgrade mode is disabled
        self.add_changelog_section(project_dir, new_version)

        # check if a project is a git repository and if so, commit bumped version changes
        if is_git_repo(project_dir):
            repo = Repo(project_dir)

            # git add
            click.echo(click.style('Staging template.', fg='blue'))
            repo.git.add(changed_files)

            # git commit
            click.echo(click.style('Committing changes to local git repository.', fg='blue'))
            repo.index.commit(f'Bump version from {self.CURRENT_VERSION} to {new_version}')

    def replace(self, file_path: str, subst: str, section: str) -> (bool, str):
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

    def can_run_bump_version(self, new_version: str, project_dir: str) -> bool:
        """
        Ensure that all requirements are met, so that the bump version command can be run successfully.
        This included the following requirements:
        1.) The new version number matches the format like 1.1.0 or 1.1.0-SNAPSHOT required by cookietemple versions
        2.) The new version is greater than the current one
        3.) The project is a cookietemple project

        :param new_version: The new version
        :param project_dir: The directory of the project
        :return: True if bump version can be run, false otherwise.
        """
        # ensure that the entered version number matches correct format like 1.1.0 or 1.1.0-SNAPSHOT but not 1.2 or 1.2.3.4
        if not re.match(r'(?<!\.)\d+(?:\.\d+){2}((?!.)|-SNAPSHOT)(?!.)', new_version):
            click.echo(click.style('Invalid version specified!\nEnsure your version number has the form '
                                   'like 0.0.0 or 15.100.239-SNAPSHOT', fg='red'))
            return False

        # ensure the version is bumped within a project created by cookietemple
        elif not Path(f'{project_dir}/cookietemple.cfg').is_file():
            click.echo(click.style('Did not found a cookietemple.cfg file. Make sure you are in the right directory '
                                   'or specify the path to your projects bump_version.cfg file', fg='red'))
            return False

        # equal versions won't be accepted for bump-version
        elif new_version == self.CURRENT_VERSION:
            click.echo(click.style(f'The new version {new_version} cannot be equal to the current version {self.CURRENT_VERSION}.', fg='red'))
            return False

        # only allow bump from a SNAPSHOT version to its correlate with -SNAPSHOT removed (like 1.0.0-SNAPSHOT to 1.0.0 but not 2.0.0)
        elif self.CURRENT_VERSION.endswith('-SNAPSHOT') and not self.CURRENT_VERSION.split('-')[0] == new_version:
            click.echo(click.style(f'Cannot bump {self.CURRENT_VERSION} to {new_version}.', fg='red') +
                       click.style(f'\n{self.CURRENT_VERSION} as a SNAPSHOT version can only be bumped to its non-snapshot correlate '
                                   f'{self.CURRENT_VERSION.split("-")[0]}.', fg='blue'))
            return False

        # ensure the new version is greater than the current one, if not the user wants to explicitly downgrade it
        elif not self.downgrade_mode:
            current_version_r = self.CURRENT_VERSION.replace('-SNAPSHOT', '')
            new_version_r = new_version.replace('-SNAPSHOT', '')

            # bump from x.x.x to x.x.x-SNAPSHOT should be only allowed when using the downgrade flag
            if new_version.endswith('-SNAPSHOT') and self.CURRENT_VERSION == new_version.split('-')[0]:
                click.echo(click.style(f'Cannot downgrade {self.CURRENT_VERSION} to its version SNAPSHOT {new_version}.', fg='red') +
                           click.style(f'\nUse the -d flag if you want to downgrade {self.CURRENT_VERSION} to its SNAPSHOT version.', fg='blue'))
                return False

            # when the current version and the new version are equal, but one is a -SNAPSHOT version return true
            elif version.parse(current_version_r) == version.parse(new_version_r) and ('-SNAPSHOT' in self.CURRENT_VERSION or '-SNAPSHOT' in new_version):
                return True

            # else check if the new version is greater than the current version
            elif version.parse(current_version_r) < version.parse(new_version_r):
                return True

            # the new version is not greater than the current one
            click.echo(click.style(f'The new version {new_version} is not greater than the current version {self.CURRENT_VERSION}.'
                                   f'\nThe new version must be greater than the old one.', fg='red'))
            return False

        return True

    def check_bump_range(self, current_version: str, new_version: str) -> bool:
        """
        Check if the new version seems to be a reasonable bump or not (ignored when using the downgrade flag).
        This should not break the bump-version process, but it requires confirmation of the user.

        :param current_version: The current version
        :param new_version: The new version
        :return: If it´s a reasonable bump
        """
        cur_v_split = current_version.split('.')
        new_v_split = new_version.split('.')

        # major update like bumping from 1.8.3 to 2.0.0
        if new_v_split[0] != cur_v_split[0]:
            return new_v_split[1] == '0' and new_v_split[2] == '0' and (int(new_v_split[0]) - int(cur_v_split[0]) == 1)

        # minor update like bumping from 1.8.5 to 1.9.0
        elif new_v_split[1] != cur_v_split[1]:
            return new_v_split[0] == cur_v_split[0] and new_v_split[2] == '0' and (int(new_v_split[1]) - int(cur_v_split[1]) == 1)

        # x-minor update like bumping from 1.8.5 to 1.8.6
        elif new_v_split[2] != cur_v_split[2]:
            return new_v_split[0] == cur_v_split[0] and new_v_split[1] == cur_v_split[1] and (int(new_v_split[2]) - int(cur_v_split[2]) == 1)

        # case when we bumping like 3.0.0-SNAPSHOT to 3.0.0
        return True

    def lint_before_bump(self) -> None:
        """
        Lint the changelog prior to bumping. Linting consists of two major points (beside checking if a CHANGELOG.rst file even exists at top level directory).

        1. Lint CHANGELOG.rst to ensure that bump-version can safely add a new section
        2. Check, whether all versions are consistent over the project
        """
        changelog_linter = TemplateLinter(path=self.top_level_dir)
        changelog_path = os.path.join(self.top_level_dir, 'CHANGELOG.rst')
        # ensure changelog exists, else abort
        if not os.path.exists(changelog_path):
            click.echo(click.style(f'No file named CHANGELOG.rst found at {self.top_level_dir}. Aborting!', fg='red'))
            sys.exit(1)
        # lint changelog and check version consistency
        changelog_linter.lint_changelog()
        changelog_linter.check_version_consistent()
        click.echo()
        changelog_linter.print_results()
        click.echo()
        # if any failed linting tests, ask user for confirmation of proceeding with bump (which results in undefined behavior)
        if len(changelog_linter.failed) > 0 or len(changelog_linter.warned) > 0:
            # ask for confirmation if the user really wants to proceed bumping when linting failed
            click.echo(click.style(f'Changelog linting and/or version check failed!\nYou can fix them and try bumping again. Proceeding bump will result in '
                                   f'undefined behavior!', fg='red'))
            if not click.confirm(click.style(f'Do you really want to continue?', fg='red')):
                sys.exit(1)

    def add_changelog_section(self, path: Path, new_version: str) -> None:
        """
        Each version bump will add a new section template to the CHANGELOG.rst
        :param path: Path to top level project directory (where the CHANGELOG.rst file should lie)
        :param new_version: The new version
        """
        if self.downgrade_mode:
            click.echo(click.style('WARNING: Running bump-version in downgrade mode will not add a new changelog section currently!', fg='yellow'))
        else:
            date = datetime.today().strftime("%Y-%m-%d")
            # replace the SNAPSHOT SECTION header with its non-snapshot correlate
            if self.CURRENT_VERSION.endswith('-SNAPSHOT'):
                self.replace_snapshot_header(f'{self.top_level_dir}/CHANGELOG.rst', new_version, date)

            else:
                # the section template for a new changelog section
                nl = '\n'
                section = f'{new_version} ({date}){nl}{"-" * (len(new_version) + len(date) + 3)}{nl}{nl}' \
                    f'{f"**{nl}{nl}".join(["**Added", "**Fixed", "**Dependencies", "**Deprecated**"])}'

                self.insert_latest_version_section(old_changelog_file=f'{self.top_level_dir}/CHANGELOG.rst', section=section)

    def replace_snapshot_header(self, source_file_path, new_version: str, date: str) -> None:
        """
        Replace the SNAPSHOT header section in CHANGELOG. The pattern (currently) cannot include any newline characters, therefore no multiline support!
        :param source_file_path: Path to source file (the path where CHANGELOG lies)
        :param new_version: The new version
        :param date: Current date
        """
        # create a temp file (requires to be explicitly deleted later)
        fh, target_file_path = mkstemp()
        # read from old file (the source file) and write into new file (the target file)
        with open(target_file_path, 'w') as target_file:
            with open(source_file_path, 'r') as source_file:
                for line in source_file:
                    pattern, subst = '', ''
                    # check if the line is a header section with SNAPSHOT version
                    if re.match(r'^(?<!\.)\d+(?:\.\d+){2}(?!\.)-SNAPSHOT \(\d\d\d\d-\d\d-\d\d\)$', line):
                        dotted_snapshot_line = source_file.readline()
                        next_new_line = source_file.readline()  # noqa: F841 necessary to omit an additional newline
                        snapshot_date = line.split('(')[1][:-2]  # extract date of SNAPSHOT version adding
                        pattern = f'{self.CURRENT_VERSION} ({snapshot_date})'
                        subst = f'{new_version} ({date})\n{(len(new_version) + len(date) + 3) * "-"}'
                        # replace -SNASPHOT in the header and adjust the dotted line below to the new header length
                        target_file.write(line.replace(pattern, subst))
                        target_file.write(dotted_snapshot_line.replace('-', ''))
                    else:
                        # else just write the line to the new file
                        target_file.write(line.replace(pattern, subst))
        # remove old file
        remove(source_file_path)
        # move new file to replace old file
        move(target_file_path, source_file_path)

    def insert_latest_version_section(self, old_changelog_file: str, section: str) -> None:
        """
        Insert the new changelog section as the latest section right after the header
        :param old_changelog_file: path to the current CHANGELOG.rst file
        :param section: the new section template block for changelog
        """
        # create a temp file (requires to be explicitly deleted later)
        fh, target_file_path = mkstemp()
        # read from old file (the source file) and write into new file (the target file)
        with open(target_file_path, 'w') as target_file:
            with open(old_changelog_file, 'r') as source_file:
                for line in source_file:
                    # check if the line is the header section with the latest version
                    if re.match(rf'^{self.CURRENT_VERSION} \(\d\d\d\d-\d\d-\d\d\)$', line):
                        target_file.write(f'{section}\n\n\n')
                    target_file.write(line)
        # remove old file
        remove(old_changelog_file)
        # move new file to replace old file
        move(target_file_path, old_changelog_file)
