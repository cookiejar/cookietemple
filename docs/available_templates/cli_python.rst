cli-python
----------

Purpose
^^^^^^^^

cli-python is a `Python <https://www.python.org/>`_ based template designed for command line applications,
but it may also be easily used as standard Python package without any command line interface. It is an improved version of `cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_.

Design
^^^^^^^^

| The Python package is based on a standard `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ structure including a :code:`setup.py`, :code:`setup.cfg`, :code:`MANIFEST.in`,
  :code:`requirements.txt` and :code:`requirements_dev.txt` file.

.. code::

    ├── AUTHORS.rst
    ├── CHANGELOG.rst
    ├── .coafile
    ├── CODEOFCONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── codeofconduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── modules.rst
    │   ├── readme.rst
    │   ├── requirements.txt
    │   └── usage.rst
    ├── .editorconfig
    ├── Exploding_Springfield
    │   ├── cli.py
    │   ├── Exploding_Springfield.py
    │   ├── files
    │   │   └── test.txt
    │   ├── __init__.py
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── build_package.yml
    │       ├── run_flake8_linting.yml
    │       ├── publish_package.yml
    │       └── run_tox_testsuite.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── MANIFEST.in
    ├── README.rst
    ├── .readthedocs.yml
    ├── requirements_dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   └── test_Exploding_Springfield.py
    ├── tox.ini
    └── .travis.yml

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ for code packaging
2. `click <https://click.palletsprojects.com/>`_, `argparse <https://docs.python.org/3/library/argparse.html>`_ or no command line interface
3. `pytest <https://docs.pytest.org/en/latest/>`_ or `unittest <https://docs.python.org/3/library/unittest.html>`_ as testing frameworks
4. Preconfigured `tox <https://tox.readthedocs.io/en/latest/>`_ to run pytest matrices with different Python environments
5. Preconfigured `readthedocs <https://readthedocs.org/>`_
6. Eight Github workflows:

  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`build_package.yml`, which builds the cli-python package.
  3. :code:`run_flake8_linting.yml`, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  4. :code:`run_tox_testsuite.yml`, which runs the tox testing suite.
  5. :code:`publish_package.yml`, which publishes the package to PyPi. Note that it only runs on Github release and requires PyPi secrets to be set up.
  6. :code:`run_codecov`, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  7. :code:`run_bandit`, run `bandit <https://github.com/PyCQA/bandit>`_ to discover security issues in your python code
  8. :code:`pr_to_master_from_patch_release_only`: Please read :ref:`pr_master_workflow_docs`.


We highly recommend to use click (if commandline interface is required) together with pytest.

Usage
^^^^^^^^

The generated cli-python project can be installed using::

    make install

or alternatively::

    python setup.py install

Your package is then installed globally (or in your virtual environment) on your machine and can be called from your favorite shell::

    <<your_project_name>>

Other make targets include::

    make clean

which removes all build files::

    make dist

which builds source and wheel packages, which can then be used for a PyPi release using

    make release

All possible Makefile commands can be viewed using::

    make help

FAQ
^^^^^^

Do I need a command line interface?
++++++++++++++++++++++++++++++++++++++++++++++

No you do not need a command line interface. cli-python can also be used as a Python package.

Does cli-python offer `Poetry <https://python-poetry.org/>`_ support?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

No, but we would like to add it in the future. Contributions are welcome!
