#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""
import os

{% if cookiecutter.testing_library == 'pytest' -%}
import pytest
{% else %}
import unittest
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner
{%- endif %}

# from {{cookiecutter.project_slug|replace('-', '_')}} import {{cookiecutter.project_slug|replace('-', '_')}}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from {{cookiecutter.project_slug|replace('-', '_')}} import cli
{%- endif %}

{%- if cookiecutter.testing_library == 'pytest' %}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    return requests.get('https://github.com/torvalds/linux')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
{%- if cookiecutter.command_line_interface|lower == 'click' %}


class UnixFS:

    @staticmethod
    def rm(filename):
        os.remove(filename)

def test_unix_fs(mocker):
    mocker.patch('os.remove')
    UnixFS.rm('file')
    os.remove.assert_called_once_with('file')


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{%- endif %}
{%- else %}


class Test{{ cookiecutter.project_slug|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.project_slug }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

def rm(filename):
    os.remove(filename)

    from unittest import mock
    class RmTestCase(unittest.TestCase):
        @mock.patch('mymodule.os')
        def test_rm(self, mock_os):
            rm("any path")
            # test that rm called os.remove with the right parameters
            mock_os.remove.assert_called_with("any path")

{%- if cookiecutter.command_line_interface|lower == 'click' %}

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
{%- endif %}
{%- endif %}
