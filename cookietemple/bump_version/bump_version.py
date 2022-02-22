import logging
import os
import re
import sys
from configparser import ConfigParser, NoSectionError
from os import fdopen, remove
from pathlib import Path
from shutil import copymode, move
from tempfile import mkstemp
from typing import Tuple

from git import Repo  # type: ignore
from packaging import version
from rich import print

from cookietemple.create.github_support import is_git_repo
from cookietemple.custom_cli.questionary import cookietemple_questionary_or_dot_cookietemple
from cookietemple.lint.template_linter import TemplateLinter

log = logging.getLogger(__name__)


class VersionBumper:
    """
    Responsible for bumping the version across a cookietemple project
    """

    def __init__(self, project_dir, downgrade):
        try:
            self.parser = ConfigParser()
            self.parser.read(f"{project_dir}/cookietemple.cfg")
            self.CURRENT_VERSION = self.parser.get("bumpversion", "current_version")
            self.downgrade_mode = downgrade
            self.top_level_dir = project_dir
        except (KeyError, NoSectionError):
            print(
                f"[bold red]No cookietemple.cfg file was found at [bold blue]{project_dir} [bold red]or your cookietemple.cfg file missing required "
                f"bump-version section.\nPlease refer to the bump-version documentation for more information!"
            )
            sys.exit(1)

    def bump_template_version(self, new_version: str, project_dir: Path, create_tag: bool) -> None:
        """
        Update the version number for all files that are whitelisted in the config file or explicitly allowed in the blacklisted section.

        Concerning valid versions: All versions must match the format like 1.0.0 or 1.1.0-SNAPSHOT; these are the only valid
        version formats cookietemple allows. A valid version therefore contains a three digits (in the range from 0 to however large it will grow)
        separated by two dots.
        Optional is the -SNAPSHOT at the end (for JVM templates especially). NOTE that versions like 1.2.3.4 or 1.2 WILL NOT be recognized as valid versions as
        well as no substring of them will be recognized.

        :param new_version: The new version number that should replace the old one in a cookietemple project
        :param project_dir: The default value is the current working directory, so we´re initially assuming the user
                             bumps the version from the projects top level directory. If this is not the case this parameter
                             shows the path where the projects top level directory is and bumps the version there
        :param create_tag: Whether to create a tag for the commit (if project has a git repo) or not
        """
        log.debug(f"Current version: {self.CURRENT_VERSION} --- New version: {new_version}")
        sections = ["bumpversion_files_whitelisted", "bumpversion_files_blacklisted"]

        # if project_dir was given as handle use cwd since we need it for git add
        ct_cfg_path = (
            f"{str(project_dir)}/cookietemple.cfg"
            if str(project_dir).startswith(str(Path.cwd()))
            else f"{str(Path.cwd())}/{project_dir}/cookietemple.cfg"
        )

        # keep path of all files that were changed during bump version
        changed_files = [ct_cfg_path]

        print(
            f"[bold blue]Changing version number.\nCurrent version is {self.CURRENT_VERSION}."
            f"\nNew version will be {new_version}\n"
        )

        # for each section (whitelisted and blacklisted files) bump the version (if allowed)
        for section in sections:
            log.debug(f"Bumping files of section: {section}.")
            for _file, path in self.parser.items(section):
                not_changed, file_path = VersionBumper.replace(f"{project_dir}/{path}", new_version, section)
                # only add file if the version(s) in the file were bumped
                if not not_changed:
                    path_changed = (
                        file_path if file_path.startswith(str(Path.cwd())) else f"{str(Path.cwd())}/{file_path}"
                    )
                    changed_files.append(path_changed)

        # update new version in cookietemple.cfg file
        log.debug("Updating version in cookietemple.cfg file.")
        self.parser.set("bumpversion", "current_version", new_version)
        # get linesep for each OS (MacOS and Linux: -1, on Windows: -2)
        remove_chars = len(os.linesep)
        with open(f"{project_dir}/cookietemple.cfg", "w") as configfile:
            self.parser.write(configfile)
            # truncates the config file and removes the last new line
            configfile.truncate(configfile.tell() - remove_chars)

        # check whether a project is a git repository and if so, commit bumped version changes
        if is_git_repo(project_dir):
            repo = Repo(project_dir)

            # git add
            print("[bold blue]Staging template")
            repo.git.add(changed_files)

            # git commit
            print("[bold blue]Committing changes to local git repository.")
            repo.index.commit(f"Bump version from {self.CURRENT_VERSION} to {new_version}")
            if create_tag:
                print("[bold blue]Creating tag for bump version commit.")
                repo.create_tag(f"{new_version}", message=f"Bump from {self.CURRENT_VERSION} to {new_version}")

    @staticmethod
    def replace(file_path: str, subst: str, section: str) -> Tuple[bool, str]:
        """
        Replace a version with the new version unless the line is explicitly excluded (marked with <<COOKIETEMPLE_NO_BUMP>>).
        In case of blacklisted files, bump-version ignores all lines with version numbers unless they´re explicitly marked
        for bump with tag <<COOKIETEMPLE_FORCE_BUMP>>.
        :param file_path: The path of the file where the version should be updated
        :param subst: The new version that replaces the old one
        :param section: The current section (whitelisted or blacklisted files)

        :return: Whether a file has been changed during bumped and the path of changed file
        """
        # flag that indicates whether no changes were made inside a file
        file_is_unchanged = True
        path_changed = ""

        # Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh, "w") as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    # update version if tags were found (and were in the right section)
                    if (
                        "<<COOKIETEMPLE_NO_BUMP>>" not in line and not section == "bumpversion_files_blacklisted"
                    ) or "<<COOKIETEMPLE_FORCE_BUMP>>" in line:
                        # for info on this regex, see bump_template docstring above
                        tmp = re.sub(r"(?<!\.)\d+(?:\.\d+){2}(?:-SNAPSHOT)?(?!\.)", subst, line)
                        new_file.write(tmp)
                        if tmp != line:
                            if file_is_unchanged:
                                print(f"[bold blue]Updating version number in {file_path}")
                                file_is_unchanged = False
                                path_changed = file_path
                            print(
                                f'[bold red]- {line.strip().replace("<!-- <<COOKIETEMPLE_FORCE_BUMP>> -->", "")}\n'
                                + f'[bold green]+ {tmp.strip().replace("<!-- <<COOKIETEMPLE_FORCE_BUMP>> -->", "")}'
                            )
                            print()
                    else:
                        new_file.write(line)
        # Copy the file permissions from the old file to the new file
        copymode(file_path, abs_path)
        # Remove original file
        remove(file_path)
        # Move new file
        move(abs_path, file_path)

        return file_is_unchanged, path_changed

    def can_run_bump_version(self, new_version: str) -> bool:
        """
        Ensure that all requirements are met, so that the bump version command can be run successfully.
        This included the following requirements:
        1.) The new version number matches the format like 1.1.0 or 1.1.0-SNAPSHOT required by cookietemple versions
        2.) The new version is greater than the current one
        3.) The project is a cookietemple project (this is already checked when creating the "bumper" object
        :param new_version: The new version

        :return: True if bump version can be run, false otherwise.
        """
        # ensure that the entered version number matches correct format like 1.1.0 or 1.1.0-SNAPSHOT but not 1.2 or 1.2.3.4
        if not re.match(r"(?<!\.)\d+(?:\.\d+){2}((?!.)|-SNAPSHOT)(?!.)", new_version):
            print(
                "[bold red]Invalid version specified!\n"
                "Ensure your version number has the form of 0.0.0 or 15.100.239-SNAPSHOT"
            )
            return False

        # equal versions won't be accepted for bump-version
        elif new_version == self.CURRENT_VERSION:
            print(
                f"[bold red]The new version {new_version} cannot be equal to the current version {self.CURRENT_VERSION}."
            )
            return False

        # only allow bump from a SNAPSHOT version to its correspondance with -SNAPSHOT removed (like 1.0.0-SNAPSHOT to 1.0.0 but not 2.0.0)
        elif self.CURRENT_VERSION.endswith("-SNAPSHOT") and not self.CURRENT_VERSION.split("-")[0] == new_version:
            print(
                f"[bold red]Cannot bump {self.CURRENT_VERSION} to {new_version}."
                + f"[blue]\n{self.CURRENT_VERSION} as a SNAPSHOT version can only be bumped to its non-snapshot equivalent "
                f'{self.CURRENT_VERSION.split("-")[0]}.'
            )
            return False

        # ensure the new version is greater than the current one, if not the user wants to explicitly downgrade it
        elif not self.downgrade_mode:
            current_version_r = self.CURRENT_VERSION.replace("-SNAPSHOT", "")
            new_version_r = new_version.replace("-SNAPSHOT", "")

            # bump from x.x.x to x.x.x-SNAPSHOT should be only allowed when using the downgrade flag
            if new_version.endswith("-SNAPSHOT") and self.CURRENT_VERSION == new_version.split("-")[0]:
                print(
                    f"[bold red]Cannot downgrade {self.CURRENT_VERSION} to its version SNAPSHOT {new_version}."
                    + f"[blue]\nUse the -d flag if you want to downgrade {self.CURRENT_VERSION} to its SNAPSHOT version."
                )
                return False

            # when the current version and the new version are equal, but one is a -SNAPSHOT version return true
            elif version.parse(current_version_r) == version.parse(new_version_r) and (
                "-SNAPSHOT" in self.CURRENT_VERSION or "-SNAPSHOT" in new_version
            ):
                return True

            # else check if the new version is greater than the current version
            elif version.parse(current_version_r) < version.parse(new_version_r):
                return True

            # the new version is not greater than the current one
            print(
                f"[bold red]The new version {new_version} is not greater than the current version {self.CURRENT_VERSION}."
                f"\nThe new version must be greater than the old one."
            )
            return False

        return True

    def check_bump_range(self, current_version: str, new_version: str) -> bool:
        """
        Check whether the new version seems to be a reasonable bump or not (ignored when using the downgrade flag).
        This should not break the bump-version process, but it requires confirmation of the user.
        :param current_version: The current version
        :param new_version: The new version

        :return: Whether it´s a reasonable bump
        """
        cur_v_split = current_version.split(".")
        new_v_split = new_version.split(".")

        # major update like bumping from 1.8.3 to 2.0.0
        if new_v_split[0] != cur_v_split[0]:
            log.debug("Identified major version bump")
            return new_v_split[1] == "0" and new_v_split[2] == "0" and (int(new_v_split[0]) - int(cur_v_split[0]) == 1)

        # minor update like bumping from 1.8.5 to 1.9.0
        elif new_v_split[1] != cur_v_split[1]:
            log.debug("Identified minor version bump")
            return (
                new_v_split[0] == cur_v_split[0]
                and new_v_split[2] == "0"
                and (int(new_v_split[1]) - int(cur_v_split[1]) == 1)
            )

        # patch update like bumping from 1.8.5 to 1.8.6
        elif new_v_split[2] != cur_v_split[2]:
            log.debug("Identified patch version bump")
            return (
                new_v_split[0] == cur_v_split[0]
                and new_v_split[1] == cur_v_split[1]
                and (int(new_v_split[2]) - int(cur_v_split[2]) == 1)
            )

        # case when we bumping like 3.0.0-SNAPSHOT to 3.0.0
        log.debug("Identified SNAPSHOT version bump")
        return True

    def lint_before_bump(self) -> None:
        """
        Check, whether all versions are consistent over the project
        """
        version_linter = TemplateLinter(path=self.top_level_dir)
        version_linter.check_version_consistent()
        print()
        version_linter.print_results()
        print()
        # if any failed linting tests, ask user for confirmation of proceeding with bump (which results in undefined behavior)
        if len(version_linter.failed) > 0 or len(version_linter.warned) > 0:
            # ask for confirmation if the user really wants to proceed bumping when linting failed
            print(
                "[bold red]Version check failed!\n"
                "You can fix them and try bumping again. Proceeding bump will result in undefined behavior!"
            )
            if not cookietemple_questionary_or_dot_cookietemple(
                function="confirm", question="Do you really want to continue?", default="n"
            ):
                sys.exit(1)

    def choose_valid_version(self) -> str:
        version_split = self.CURRENT_VERSION.split(".")
        new_patch, new_minor, new_major = (
            str(int(version_split[2]) + 1),
            str(int(version_split[1]) + 1),
            str(int(version_split[0]) + 1),
        )
        version_split_patch = [version_split[0], version_split[1], new_patch]
        version_split_minor = [version_split[0], new_minor, "0"]
        version_split_major = [new_major, "0", "0"]

        new_version = cookietemple_questionary_or_dot_cookietemple(
            function="select",
            question="Choose the new project version:",
            choices=[".".join(version_split_patch), ".".join(version_split_minor), ".".join(version_split_major)],
            default="cli",
        )
        return new_version  # type:ignore
