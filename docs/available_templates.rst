.. _available_templates:

=========================
Available templates
=========================

COOKIETEMPLE currently has the following templates available:

1. `cli-python`_
2. `cli-java`_
3. `cli-kotlin`_
4. `web-website-python`_
5. `gui-java`_
6. `gui-kotlin`_
7. `pub-thesis-latex`_

In the following every template is devoted its own section, which explains its purpose, design, included frameworks/libraries and usage.

cli-python
----------

Purpose
++++++++

cli-python is a `Python <https://www.python.org/>`_ based template for designed for command line applications,
but it may also be easily used as standard Python package without any command line interface.

Design
++++++++

| The Python package is based on a standard `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ structure including a :code:`setup.py`, :code:`setup.cfg`, :code:`MANIFEST.in`,
  :code: `requirements.txt` and :code:`requirements_dev.txt` file.
| The main code resides in a folder, which shares the name of the *project_slug*.
   Inside the *project_slug* folder :code:`cli.py` hosts any command line interface code, :code:`project_slug.py` includes any module code.
   The folder :code:`files` can be used to include any files, which should also be included in the Python package.
   Note, that if the folder is renamed or moved that this has to be reflected in the :code:`setup.py` file.
| The folder :code:`tests` includes all unit tests.

Included frameworks/libraries
+++++++++++++++++++++++++++++

| cli-python is based on `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ to package its code.
| Three (two) options are available as command line interfaces: `click <https://click.palletsprojects.com/>`_, `argparse <https://docs.python.org/3/library/argparse.html>`_ or no command line interface.
| `pytest <https://docs.pytest.org/en/latest/>`_ and `unittest <https://docs.python.org/3/library/unittest.html>`_ are the available testing frameworks. Moreover, `tox <https://tox.readthedocs.io/en/latest/>`_ is already preconfigured and runs pytest matrices to test different Python environments.
  We highly recommend to use click together with pytest.
| Preconfigured `readthedocs <https://readthedocs.org/>`_ is also included in the template.
| The template also ships with five Github workflows:
  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`build_package.yml`, which builds the cli-python package.
  3. :code:`flake8_linting.yml`, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  4. :code:`tox_testsuite.yml`, which runs the tox testing suite.
  5. :code:`publish_package.yml`, which publishes the package to PyPi. Note that it only runs on Github release and requires PyPi secrets to be set up.

Usage
+++++++

The generated cli-python project can be installed using::

    make install

or alternatively::

    python setup.py install

Your package is then installed globally (or in your virtual environment) on your machine and can be called from your favorite shell::

    project_slug

Other make targets include::

    make clean

which removes all build files::

    make dist

which builds source and wheel packages, which can then be used for a PyPi release using

    make release

All possible Makefile commands can be viewed using::

    make help

cli-java
---------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++

cli-kotlin
------------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++

web-website-python
-------------------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++

gui-java
---------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++

gui-kotlin
-------------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++

pub-thesis-latex
--------------------

Purpose
++++++++

Design
++++++++

Included frameworks/libraries
+++++++++++++++++++++++++++++

Usage
+++++++
