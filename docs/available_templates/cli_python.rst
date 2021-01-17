cli-python
----------

Purpose
^^^^^^^^

cli-python is a `Python <https://www.python.org/>`_ based template designed for command line applications,
but it may also be easily used as standard Python package without any command line interface. It is an improved version of `cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_.

Design
^^^^^^^^

| The Python package is based on a standard `poetry <https://python-poetry.org/>`_ structure with a corresponding ``pyproject.toml`` and ``poetry.lock`` file.

.. code::

    ├── AUTHORS.rst
    ├── .bandit.yml
    ├── CHANGELOG.rst
    ├── codecov.yml
    ├── CODE_OF_CONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .darglint
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── code_of_conduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── readme.rst
    │   ├── reference.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── .flake8
    ├── .gitattributes
    ├── .github
    │   ├── dependabot.yml
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── labels.yml
    │   ├── pull_request_template.md
    │   ├── release-drafter.yml
    │   └── workflows
    │       ├── build_package.yml
    │       ├── check_no_SNAPSHOT_master.yml
    │       ├── check_patch_release_master_only.yml
    │       ├── constraints.txt
    │       ├── labeler.yml
    │       ├── publish_docs.yml
    │       ├── publish_package.yml
    │       ├── run_cookietemple_lint.yml
    │       ├── run_tests.yml
    │       └── sync_project.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── makefiles
    │   ├── Linux.mk
    │   └── Windows.mk
    ├── mypy.ini
    ├── noxfile.py
    ├── poetry.lock
    ├── .pre-commit-config.yaml
    ├── .prettierignore
    ├── pyproject.toml
    ├── README.rst
    ├── .readthedocs.yml
    ├── src
    │   └── project_name
    │       ├── __init__.py
    │       ├── __main__.py
    │       └── py.typed
    └── tests
        ├── __init__.py
        └── test_main.py


Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `poetry <https://setuptools.readthedocs.io/en/latest/>`_ for code packaging
2. `click <https://click.palletsprojects.com/>`_ or no command line interface
3. `pytest <https://docs.pytest.org/en/latest/>`_ or `unittest <https://docs.python.org/3/library/unittest.html>`_ as testing frameworks
4. `nox <https://nox.thea.codes/en/stable/>`_ to automate testing in multiple Python environments
5. `pre-commit <https://pre-commit.com/>`_ to run various code style linters and to enforce a common style
6. Preconfigured `readthedocs <https://readthedocs.org/>`_
7. Eight Github workflows:

  1. ``build_docs.yml``, which builds the readthedocs documentation.
  2. ``build_package.yml``, which builds the cli-python package.
  3. ``publish_package.yml``, which publishes the package to PyPi. Note that it only runs on Github release and requires PyPi secrets to be set up.
  4. ``run_tests``, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  5. ``pr_to_master_from_patch_release_only``: Please read :ref:`pr_master_workflow_docs`.
  6. ``check_no_SNAPSHOT_master.yml``: Please read :ref:`pr_master_workflow_docs`
  7. ``run_cookietemple_lint.yml``, which runs ``cookietemple lint`` on the project.
  8. ``sync_project.yml``, which syncs the project to the most recent cookietemple template version


We highly recommend to use click (if commandline interface is required) together with pytest.

Usage
^^^^^^^^

The generated cli-python project can be installed using::

    make install

or alternatively::

    poetry install

Your package is then installed in a custom virtual environment on your machine and can be called from your favorite shell::

    <<your_project_name>>

Other make targets include::

    make clean

which removes all build files::

    make build

which builds source and wheel packages, which can then be used for a PyPi release using

    make release

All possible Makefile commands can be viewed using::

    make help

FAQ
^^^^^^

Do I need a command line interface?
++++++++++++++++++++++++++++++++++++++++++++++

No you do not need a command line interface. cli-python can also be used as a Python package.
