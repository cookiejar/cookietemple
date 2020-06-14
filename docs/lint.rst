.. _lint:

=====================
Linting your project
=====================

`Linting <https://en.wikipedia.org/wiki/Lint_(software)>`_ is the process of statically analyzing code to find code style violations and to detect errors.
COOKIETEMPLE implements a custom linting system, but depending on the template external tools linting tools may be additionally be called.

COOKIETEMPLE linting
-----------------------

COOKIETEMPLE lint can be invoked on an existing project using

.. code-block:: console

    cookietemple lint <OPTIONS> <PATH>

COOKIETEMPLE's linting is divided into three distinct phases.

1. All linting functions, which all templates share are called and the results are collected.
2. Template specific linting functions are invoked and the results are appended to the results of phase 1
3. Template specific external linters are called (e.g. autopep8 for Python based projects)

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

   Linting applied to a newly created cli-java project.

To examine the reason for a failed linting test please follow the URL. All reasons are explained in the section :ref:`linting_codes`.

Linting codes
-----------------

TODO
