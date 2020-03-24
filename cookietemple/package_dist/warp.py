import os
import stat
from pathlib import Path
from subprocess import Popen, PIPE
from sys import platform

import click
from ruamel.yaml import YAML

WD = os.path.dirname(__file__)

def warp_project(input_dir: str, exec: str, output: str) -> None:
    """
    Packages a JVM based project into a single executable using Warp (https://github.com/dgiagio/warp).
    Requires a JRE to be bundled with the project.
    Warp is bundled with COOKIETEMPLE, does however require executable permissions to be set, which COOKIETEMPLE also prompts for
    """
    WARP_INFO_PATH = f'{WD}/warp/warp_info.yml'
    WARP_LINUX_PATH = f'{WD}/warp/linux-x64.warp-packer'
    WARP_MACOS_PATH = f'{WD}/warp/macos-x64.warp-packer'
    WARP_WINDOWS_PATH = f'{WD}/warp/windows-x64.warp-packer.exe'

    # Fetch and print Warp info
    yaml = YAML(typ='safe')
    warp_info = yaml.load(Path(WARP_INFO_PATH))
    click.echo(click.style(f'Packaging using {warp_info["name"]} version: {warp_info["version"]}', fg='blue'))
    click.echo(click.style(f'For more details please visit:    {warp_info["url"]}    for more information.', fg='blue'))

    # Depending on the platform we need to call different Warp executables and handle permissions differently!
    click.echo(click.style(f'Detected {platform}', fg='blue'))
    if platform == 'linux' or platform == 'linux2':
        run_unix_warp(WARP_LINUX_PATH, 'linux-x64', input_dir, exec, output)
    elif platform == 'darwin':
        run_unix_warp(WARP_MACOS_PATH, 'macos-x64', input_dir, exec, output)
    elif platform == 'win32' or platform == 'win64':
        click.echo(click.style('Warning! Windows support is experimental! Consider using Linux', fg='blue'))


def run_unix_warp(warp_unix_path: str, arch: str, input_dir: str, exec: str, output: str) -> None:
    """
    Sets executable permissions for Warp if required and runs Warp on the target project.

    :param warp_unix_path: Path to the unix (Linux, MacOS) Warp executable
    """

    # Set Warp to be executable if it not already is. May prompt the user for sudo permissions.
    # Note: The installation should automatically set the permissions to 755, which should be sufficent for warp
    if stat.S_IXUSR & os.stat(warp_unix_path)[stat.ST_MODE]:
        click.echo(click.style(f'{warp_unix_path}\nis already executable! Will not attempt to change permissions.', fg='blue'))
    else:
        click.echo(click.style(f'{warp_unix_path}\nis NOT already executable! Will now attempt to add executable permissions to Warp.', fg='blue'))
        click.echo(click.style('You may be asked to enter your \'sudo\' password!', fg='blue'))

        # Warp is not already executable
        set_warp_executable = Popen(['sudo', 'chmod', '+x', warp_unix_path], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        (set_warp_executable_stdout, set_warp_executable_stderr) = set_warp_executable.communicate()
        if set_warp_executable.returncode != 0:
            click.echo(click.style('Unable to change file permissions of Warp!', fg='red'))
            click.echo(click.style(f'Run command was: \'sudo chmod +x {warp_unix_path}\'', fg='red'))
            click.echo(click.style(f'Error was: {set_warp_executable.stderr}', fg='red'))

    # Run Warp
    warp_run = Popen([warp_unix_path, '--arch', arch, '--input_dir', input_dir, '--exec', exec, '--output', output],
                     stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (warp_run_stdout, warp_run_stderr) = warp_run.communicate()
    click.echo(click.style(warp_run_stdout, fg='blue'))


def run_windows_warp(warp_windows_path: str) -> None:
    click.echo(click.style('Not yet implemented!', fg='red'))
