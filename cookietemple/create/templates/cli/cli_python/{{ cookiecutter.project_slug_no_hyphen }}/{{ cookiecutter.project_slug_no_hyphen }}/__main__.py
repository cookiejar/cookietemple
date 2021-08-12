#!/usr/bin/env python
"""Command-line interface."""
import click
from rich import traceback


@click.command()
@click.version_option(version="{{ cookiecutter.version }}", message=click.style("{{ cookiecutter.project_name }} Version: {{ cookiecutter.version }}"))
def main() -> None:
    """{{ cookiecutter.project_name }}."""


if __name__ == "__main__":
    traceback.install()
    main(prog_name="{{ cookiecutter.project_name }}")  # pragma: no cover
