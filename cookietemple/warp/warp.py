import os
import stat
from pathlib import Path
from subprocess import PIPE, Popen
from sys import platform

from rich import print
from ruamel.yaml import YAML

WD = os.path.dirname(__file__)


def warp_project(input_dir: str, exec: str, output: str) -> None:
    """
    Packages a JVM based project into a single executable using Warp (https://github.com/dgiagio/warp).
    Requires a JRE to be bundled with the project.
    Warp is bundled with cookietemple, does however require executable permissions to be set, which cookietemple also prompts for
    """
    WARP_INFO_PATH = f"{WD}/warp_executables/warp_info.yml"
    WARP_LINUX_PATH = f"{WD}/warp_executables/linux-x64.warp-packer"
    WARP_MACOS_PATH = f"{WD}/warp_executables/macos-x64.warp-packer"
    WARP_WINDOWS_PATH = f"{WD}/warp_executables/windows-x64.warp-packer.exe"

    # Fetch and print Warp info
    yaml = YAML(typ="safe")
    warp_info = yaml.load(Path(WARP_INFO_PATH))
    print(f'[bold blue]Packaging using {warp_info["name"]} version: {warp_info["version"]}')
    print(f'[bold blue]For more details please visit:    {warp_info["url"]}    for more information.')

    # Depending on the platform we need to call different Warp executables and handle permissions differently!
    print(f"[bold green]Detected {platform}")
    if platform == "linux" or platform == "linux2":
        run_unix_warp(WARP_LINUX_PATH, "linux-x64", input_dir, exec, output)
    elif platform == "darwin":
        run_unix_warp(WARP_MACOS_PATH, "macos-x64", input_dir, exec, output)
    elif platform == "win32" or platform == "win64":
        print(
            "[bold yellow]Warning! Windows support is experimental! Consider using Linux or running Warp as a standalone"
        )
        run_warp(WARP_WINDOWS_PATH, "windows-x64", input_dir, exec, output)


def run_unix_warp(warp_unix_path: str, arch: str, input_dir: str, exec: str, output: str) -> None:
    """
    Sets executable permissions for Warp if required and runs Warp on the target project.

    :param warp_unix_path: Path to the Warp executable
    :param arch: Operating system architecture -> one of linux-x64 or macos-x64
    :param input_dir: Path of input directory
    :param exec: Path to executable to package
    :param output: Output path
    """

    # Set Warp to be executable if it not already is. May prompt the user for sudo permissions.
    # Note: The installation should automatically set the permissions to 755, which should be sufficent for warp
    if stat.S_IXUSR & os.stat(warp_unix_path)[stat.ST_MODE]:
        print(f"[bold blue]{warp_unix_path}\nis already executable! Will not attempt to change permissions.")
    else:
        print(
            f"[bold blue]{warp_unix_path}\nis NOT already executable! Will now attempt to add executable permissions to Warp."
        )
        print("[bold blue]You may be asked to enter your 'sudo' password!")

        # Warp is not already executable
        set_warp_executable = Popen(
            ["sudo", "chmod", "+x", warp_unix_path], stdout=PIPE, stderr=PIPE, universal_newlines=True
        )
        (set_warp_executable_stdout, set_warp_executable_stderr) = set_warp_executable.communicate()
        if set_warp_executable.returncode != 0:
            print("[bold red]Unable to change file permissions of Warp!")
            print("[bold red]Run command was: 'sudo chmod +x {warp_unix_path}'")
            print("[bold red]Error was: {set_warp_executable.stderr}")

    run_warp(warp_unix_path, arch, input_dir, exec, output)


def run_warp(warp_executable_path, arch: str, input_dir: str, exec: str, output: str) -> None:
    """
    Runs Warp on the target architecture

    :param warp_executable_path: Path to the Warp executable
    :param arch: Target architecture: linux-x64, macos-x64 or windows-x64
    :param exec: Executable to be packed
    :param input_dir: Input directory
    :param output: Output binary name
    """
    warp_run = Popen(
        [warp_executable_path, "--arch", arch, "--input_dir", input_dir, "--exec", exec, "--output", output],
        universal_newlines=True,
    )
    (warp_run_stdout, warp_run_stderr) = warp_run.communicate()
