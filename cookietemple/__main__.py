#!/usr/bin/env python
"""Command-line interface."""
import click
from rich import traceback


@click.command()
@click.version_option(version="1.4.0", message=click.style("cookietemple Version: 1.4.0"))
def main() -> None:
    """cookietemple."""


if __name__ == "__main__":
    traceback.install()
    main(prog_name="cookietemple")  # pragma: no cover
