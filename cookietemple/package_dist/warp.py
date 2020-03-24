import os
from pathlib import Path
from subprocess import Popen, PIPE
from sys import platform

import click
from ruamel.yaml import YAML

WD = os.path.dirname(__file__)
WARP_FOLDER_PATH = f'{WD}/warp'


def warp_project(input_dir: str, exec: str, output: str) -> None:
    """
    Packages a JVM based project into a single executable using Warp (https://github.com/dgiagio/warp).
    Requires a JRE to be bundled with the project.
    Warp is bundled with COOKIETEMPLE, does however require executable permissions to be set, which COOKIETEMPLE also prompts for
    """
    WARP_INFO_PATH = f'{WARP_FOLDER_PATH}/warp_info.yml'
    WARP_LINUX_PATH = f'{WARP_FOLDER_PATH}/linux-x64.warp-packer'
    WARP_MACOS_PATH = f'{WARP_FOLDER_PATH}/macos-x64.warp-packer'
    WARP_WINDOWS_PATH = f'{WARP_FOLDER_PATH}/windows-x64.warp-packer.exe'

    # Fetch and print Warp info
    yaml = YAML(typ='safe')
    warp_info = yaml.load(Path(WARP_INFO_PATH))
    click.echo(click.style(f'Packaging using {warp_info["name"]} version: {warp_info["version"]}', fg='blue'))
    click.echo(click.style(f'For more details please visit:    {warp_info["url"]}', fg='blue'))

    # Depending on the platform we need to call different Warp executables
    # NOTE: Windows support is experimental, since we may run into permission issues!
    click.echo(click.style(f'Detected {platform}', fg='blue'))
    if platform == 'linux' or platform == 'linux2':
        run_warp(WARP_LINUX_PATH, 'linux-x64', input_dir, exec, output)
    elif platform == 'darwin':
        run_warp(WARP_MACOS_PATH, 'macos-x64', input_dir, exec, output)
    elif platform == 'win32' or platform == 'win64':
        click.echo(click.style('Warning! Windows support is experimental! Consider using Linux or running Warp as a standalone.', fg='blue'))
        run_warp(WARP_WINDOWS_PATH, 'windows-x64', input_dir, exec, output)


def run_warp(warp_executable_path: str, arch: str, input_dir: str, exec: str, output: str) -> None:
    """
    Runs Warp on the target project.

    :param warp_executable_path: Path to the unix (Linux, MacOS) Warp executable
    """

    warp_run = Popen([warp_executable_path, '--arch', arch, '--input_dir', input_dir, '--exec', exec, '--output', output],
                     stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (warp_run_stdout, warp_run_stderr) = warp_run.communicate()
    click.echo(click.style(warp_run_stdout, fg='blue'))
