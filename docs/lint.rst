.. _lint:

=====================
Linting your project
=====================

`Linting <https://en.wikipedia.org/wiki/Lint_(software)>`_ is the process of statically analyzing code to find code style violations and to detect errors.
cookietemple implements a custom linting system, but depending on the template external tools linting tools may additionally be called.

cookietemple's linting is divided into three distinct phases.

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

Usage
--------

cookietemple lint can be invoked on an existing project using

.. code-block:: console

    $ cookietemple lint <PATH>

- ``PATH`` [CWD]: The relative path to the project directory.

Flags
---------

- ``skip-external``: Skips any external linters such as ``autopep8``.


.. _linting_codes:

Linting codes
-----------------

The following error numbers correspond to errors found during linting.
If you are not sure why a specific linting error has occured you may find more information using the respective error code.

General
^^^^^^^^^

general-1
~~~~~~~~~~

| File not found. This error occurs when your project does not include all of cookietemple's files, which all templates share.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!

general-2
~~~~~~~~~

| Dockerfile invalid. This error usually originates from empty Dockerfiles or missing FROM statements.

general-3
~~~~~~~~~

| TODO string found. The origin of this error are ``COOKIETEMPLE TODO:`` or ``TODO COOKIETEMPLE:`` strings in the respective files. Usually, they point to things that should be
  manually configured or require other attention. You may remove them if there is no task for you to be solved.

general-4
~~~~~~~~~

| Cookiecutter string found. This error occurs if something went wrong at the project creation stage. After a project has been created using cookietemple
  there should not be any jinja2 syntax statements left. Web development templates may pose exceptions. However, ``{{ *cookiecutter* }}`` statements
  should definitely not be present anymore.

general-5
~~~~~~~~~~

| Versions not consistent. If the version of all files specified in the [bumpversion] sections defined in the qube.cfg file are not consistent,
  this error may be found. Please ensure that the version is consistent! If you need to exclude specific lines from this check please consult :ref:`bump-version`.
  To prevent this error you should only increase the version of your project using :code:`cookietemple bump-version`.

general-6
~~~~~~~~~~~~~

| ``changelog.rst`` invalid. The ``changelog.rst`` file requires that every changelog section has a header with the version and the corresponding release date.
  The version above another changelog section should always be *greater* than the section below (e.g. 1.1.0 above 1.0.0).
  Every section must have the headings ``**Added**``, ``**Fixed**``, ``**Dependencies**`` and ``**Deprecated**``.

general-7
~~~~~~~~~~~~~

| ``cookietemple.cfg`` linting failed. The ``cookietemple.cfg`` plays a major role in cookietemple's ``sync`` and ``bump-version`` functionality.

The linter ensures that following requirements are met:


1.) Every config file should have at least the following sections: ``bumpversion, bumpversion_files_whitelisted, bumpversion_files_blacklisted, sync_files_blacklisted, sync_level``

2.) ``bumpversion`` should only contain a ``current_version`` value (the project's current version)

3.) ``bumpversion_files_whitelisted`` should contain at least the ``.cookietemple.yml`` file in the ``dot_cookietemple`` variable

4.) ``sync_level`` should only contain a ``ct_sync_level`` value (and this value should be one of either ``patch``, ``minor`` or ``major``)

5.) ``sync_files_blacklisted`` should contain at least the ``CHANGELOG.rst`` file (excluding it from syncing to avoid PR updates)


cli-python
^^^^^^^^^^^^

cli-python-1
~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of cli-python's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!

cli-python-2
~~~~~~~~~~~~~~~

| PyPI dependency not up to date. The dependencies specified in the requirements.txt and requirements_dev.txt are not up to date.
| It is up to you whether you can and want to update them.

cli-java
^^^^^^^^^^^^

cli-java-1
~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of cli-java's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!

lib-cpp
^^^^^^^^^^

lib-cpp-1
~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of lib-cpp's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!


web-python
^^^^^^^^^^^^

web-python-1
~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of web-python's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!

gui-java
^^^^^^^^^

gui-java-1
~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of gui-java's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!


pub-thesis
^^^^^^^^^^^^^

pub-thesis-1
~~~~~~~~~~~~~~~~~~~~~

| File not found. This error occurs when your project does not include all of pub-thesis's expected files.
| Please create the file and populate it with appropriate values. You should also critically reflect why it is missing, since
  at the time of the project creation using cookietemple this file should not have been missing!
