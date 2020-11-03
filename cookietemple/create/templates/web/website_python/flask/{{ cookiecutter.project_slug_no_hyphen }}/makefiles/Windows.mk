.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	if exist build rd /s /q build
	if exist dist rd /s /q dist
	if exist .eggs rd /s /q .eggs
	for /d /r . %%d in (*egg-info) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"
	del /q /s /f .\*.egg

clean-pyc: ## remove Python file artifacts
	del /s /f /q .\*.pyc
	del /s /f /q .\*.pyo
	del /s /f /q .\*~
	for /d /r . %%d in (*__pycache__) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"

clean-test: ## remove test and coverage artifacts
	if exist .tox rd /s /q .tox
	if exist .coverage rd /s /q .coverage
	if exist htmlcov rd /s /q htmlcov
	if exist .pytest_cache rd /s /q .pytest_cache

lint: ## check style with flake8
	flake8 {{cookiecutter.project_slug}} tests

test: ## run tests quickly with the default Python
{%- if cookiecutter.testing_library == 'pytest' %}
	pytest
{%- else %}
	python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	{%- if cookiecutter.testing_library == 'pytest' %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
	{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} setup.py test
	{%- endif %}
	coverage report -m
	coverage html
	$(BROWSER) htmlcov\index.html

docs: ## generate Sphinx HTML documentation, including API docs
	del /f /q docs\{{cookiecutter.project_slug}}.rst
	del /f /q docs\modules.rst
	sphinx-apidoc -o docs\ {{cookiecutter.project_slug}}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs\_build\html\index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist\*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel

install: clean ## install the package to the active Python's site-packages
	pip install .
{%- if cookiecutter.setup_type == 'advanced' %}
init_db:
	export FLASK_APP={{ cookiecutter.project_slug_no_hyphen }}\app.py; \
	flask db init; \
	flask db migrate -m"Init User Table"; \
	flask db upgrade;{% endif %}
