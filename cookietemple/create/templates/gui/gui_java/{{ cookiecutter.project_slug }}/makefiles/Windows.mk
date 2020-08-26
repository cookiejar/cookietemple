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
	mvn clean

# lint: ## check style

test: clean ## run tests quickly with the default Java
	mvn test

verify: clean ## verify is more strict than test
	mvn verify

# coverage: ## check code coverage quickly with the default Python

compile: clean
	mvn compile

binary: dist ## creates a self contained, platform specific executable with bundled JRE
	cookietemple warp --input_dir target\{{ cookiecutter.project_slug }}\ --exec bin\launcher --output {{ cookiecutter.project_slug }}.bin

dist: clean ## builds source and wheel package
	mvn javafx:jlink

install: clean ## install the package to the active local Maven repository
	mvn install

docs: ## generate Sphinx HTML documentation, including API docs
	del /f /q docs\{{ cookiecutter.project_slug }}.rst
	del /f /q docs\modules.rst
	sphinx-apidoc -o docs\ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs\_build\html\index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
