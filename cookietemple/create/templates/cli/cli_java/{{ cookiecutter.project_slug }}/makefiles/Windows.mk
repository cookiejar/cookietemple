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

clean:  ## remove all build, test, coverage and Maven artifacts
	gradle clean

# lint: ## check style

test: clean ## run tests quickly with the default Java
	gradle test

check: clean ## check is more strict than test
	gradle check

# coverage: ## check code coverage quickly with Cobertura

compile: clean
	gradle compileJava

binary: dist ## creates a self contained, platform specific executable with bundled JRE


dist: clean ## builds the binary executable
	gradle build

run: dist ## builds the binary and runs it
	.\build\native-image\{{ cookiecutter.project_slug }}

install: clean ## install the package to the active local Maven repository
	printf "\nNot available! Please run 'make binary!'"

docs: ## generate Sphinx HTML documentation, including API docs
	del /q /s /f docs\{{ cookiecutter.project_slug }}.rst
	del /q /s /f docs\modules.rst
	sphinx-apidoc -o docs\{{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs\_build\html\index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
