.. _lint:

=====================
Linting your project
=====================

| `Linting <https://en.wikipedia.org/wiki/Lint_(software)>`_ is the process of statically analyzing code to find code style violations and to detect errors.
| COOKIETEMPLE implements a custom linting system, but depending on the template external tools liting tools may be additionally be called.
| Furthermore, COOKIETEMPLE ships with `coala <https://github.com/coala/coala>`_ in the full version including all `coala-bears <https://github.com/coala/coala-bears>`_.
  Hence, :code:`coala` can optionally be run on all templates, which include a ``.coa`` file.

COOKIETEMPLE linting
-----------------------

COOKIETEMPLE lint can be invoked on an existing project using::

    cookietemple lint <OPTIONS> <PATH>

COOKIETEMPLE's linting is divided into four distinct phases.

1. All linting functions, which all templates share are called and the results are collected.
2. Template specific linting functions are invoked and the results are appended to the results of phase 1
3. Template specific external linters are called (e.g. autopep8 for Python based projects)
4. `coala <https://github.com/coala/coala>`_ is called in an interactive manner

The linting results of the first two phases are assigned into 3 groups:

.. raw:: html

    <style> .green {color:#008000; } </style>
    <style> .yellow {color:#ffff00; } </style>
    <style> .red {color:#aa0060; } </style>

.. role:: green
.. role:: yellow
.. role:: red

1. :green:`Passed`
2. :yellow:`Passed with warning`
3. :red:`Failed`

If any of the checks failed linting stops and returns an error code.

.. figure:: images/linting_example.png
   :scale: 100 %
   :alt: Linting example

   Linting applied to a newly created cli-python project.

To examine the reason for a failed linting test please follow the URL. All reasons are explained in the section :ref:`linting_codes`.

Running coala
-----------------

| `coala <https://github.com/coala/coala>`_ provides a unified command line interface for linting and interactive code fixing for several programming languages and file types.
| It is based on `coala-bears <https://github.com/coala/coala-bears>`_, which wrap an existing linter inside coala. All parameters for the linters are then defined in a .coa file, which are usually included with our templates.
| For more information, please visit the `coala website <https://coala.io/#/home>`_.

To invoke linting with coala support, please invoke::

    $ cookietemple lint --run-coala <PATH>

| Since coala is not all that well maintained anymore and clashes with our dependency versions (click), we may remove coala support in the future.

.. _linting_codes:

Linting codes
-----------------

TODO
