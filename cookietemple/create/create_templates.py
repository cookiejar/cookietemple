import os
import sys


import click

from cookiecutter.main import cookiecutter

from cookietemple.create.create_config import TEMPLATE_STRUCT



def create_template_with_subdomain(domain_path: str, subdomain: str, language: str) -> None:
    """
    Creates a chosen template that **does** have a subdomain.
    Calls cookiecutter on the main chosen template.

    :param domain_path: Path to the template, which is still in cookiecutter format
    :param subdomain: Subdomain of the chosen template
    :param language: Primary chosen language
    """
    occupied = os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
    if occupied:
        directory_exists_warning()

        if click.confirm('Do you really want to continue?'):
            cookiecutter(f'{domain_path}/{subdomain}_{language}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=TEMPLATE_STRUCT)

        else:
            click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
            sys.exit(0)
    else:
        cookiecutter(f'{domain_path}/{subdomain}_{language}',
                     no_input=True,
                     overwrite_if_exists=True,
                     extra_context=TEMPLATE_STRUCT)


def create_template_with_subdomain_framework(domain_path: str, subdomain: str, language: str, framework: str) -> None:
    """
    Creates a chosen template that **does** have a subdomain.
    Calls cookiecutter on the main chosen template.

    :param domain_path: Path to the template, which is still in cookiecutter format
    :param subdomain: Subdomain of the chosen template
    :param language: Primary chosen language
    :param framework: Chosen framework
    """
    occupied = os.path.isdir(f"{os.getcwd()}/{TEMPLATE_STRUCT['project_slug']}")
    if occupied:
        directory_exists_warning()

        if click.confirm('Do you really want to continue?'):
            cookiecutter(f'{domain_path}/{subdomain}_{language}/{framework}',
                         no_input=True,
                         overwrite_if_exists=True,
                         extra_context=TEMPLATE_STRUCT)

        else:
            click.echo(click.style('Aborted! Canceled template creation!', fg='red'))
            sys.exit(0)
    else:
        cookiecutter(f'{domain_path}/{subdomain}_{language}/{framework}',
                     no_input=True,
                     overwrite_if_exists=True,
                     extra_context=TEMPLATE_STRUCT)


def directory_exists_warning() -> None:
    """
    Prints warning that a directory already exists and any further action on the directory will overwrite its contents.
    """

    click.echo(click.style('WARNING: ', fg='red')
               + click.style(f"A directory named {TEMPLATE_STRUCT['project_slug']} already exists at", fg='red')
               + click.style(f'{os.getcwd()}', fg='green'))
    click.echo()
    click.echo(click.style('Proceeding now will overwrite this directory and its content!', fg='red'))
    click.echo()
