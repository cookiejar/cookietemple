.. _sync:

=======================
Syncing your project
=======================

Syncing is supposed to integrate any changes to the cookietemple templates back into your already existing project.
When ``cookietemple sync`` is invoked, cookietemple checks whether a new version of the corresponding template for the current project is available.
If so, cookietemple creates a temporary project with the most recent template and pushes it to the ``TEMPLATE`` branch.
Next, a pull request is submitted to the ``development`` branch.
Please note that the required ``CT_SYNC_TOKEN`` (see below) is automatically set and manual syncing should be avoided if possible.


The syncing process is configurable by setting the desired lower syncing boundary level and blacklisting files from syncing (see :ref:`sync_config`).

Requirements for sync
------------------------

For syncing to work properly, your project has to satisfy a few things:

 1. A Github repository with your projects code (private or public, organization or non-organization repository).

 2. An unmodified ``.cookietemple.yml`` file. If you modify this file, which you should never do, syncing may not be able to recreate the project with the most recent template.

 3. An active repository secret called ``CT_SYNC_TOKEN`` for your project's repository containing the encrypted personal access token with at least ``repo`` scope.

 4. A running, unmodified workflow called ``sync_project.yml``. Modifying this workflow should never be done and results in undefined sync behaviour.

Points 3 and 4 are only required when not syncing manually.


Usage
---------

To sync your project manually, simply run

.. code-block:: console

    $ cookietemple sync [PROJECT_DIR] [PAT] [GITHUB_USERNAME]

- ``PROJECT_DIR`` [CWD] : The path to the ``cookietemple.cfg`` file.

- ``PAT`` [Configured pat] : A Github personal access token with at least the ``repo`` scope. The ``sync_project.yml`` Github workflow uses the PAT set as a Github secret.

- ``GITHUB_USERNAME`` [Configured username] : The Github username to submit a pull request from. The supplied PAT has to be associated with this username.

Flags
-------

- ``--set-token`` : Update ``CT_SYNC_SECRET`` of your project's repo to a new PAT. Note that the Github username and the PAT must still match for automatic syncing to work.

- ``check-update`` : Check, whether a new release of a template for an already existing project is available.

Configuring sync
-----------------------

.. _sync_config:

Enable/Disable sync
~~~~~~~~~~~~~~~~~~~

Cookietemple aims to provide the user as much configuration as possible. So, the sync feature is optional and should also
be switched on or off. If you want to enable sync (which is the default), the ``sync_enable`` accepts the following values: ``True, true, Yes, yes, Y, y``. To disable sync,
simply change this value into one of ``False, false, No, no, N, n``. It can be configured in the::

    [sync]
    sync_enable = True

section.


Sync level
~~~~~~~~~~~~~~~~

Since cookietemple strongly adheres to semantic versioning our templates do too.
Hence, it is customizable whether only major, minor or patch releases of the template should trigger cookietemple sync.
The sync level therefore specifies a lower boundary. It can be configured in the::

    [sync_level]
    ct_sync_level = minor

section.

Blacklisting files
~~~~~~~~~~~~~~~~~~~~

Although, cookietemple only submits pull requests for files, which are part of the template, sometimes even those files should be ignored.
Examples could be any html files, which, at some point, contain only custom content and should not be synced.
When syncing, cookietemple examines the ``cookietemple.cfg`` file and ignores any file patterns (globs) (e.g. ``*.html``) below the ``[sync_files_blacklisted]`` section.
IMPORTANT NOTE: If you would like to add some files to this section, make sure your current branch (if you are syncing manually, which is not recommended) or your default branch
has the latest blacklisted sync file section with your changes, so it will be used by the sync.
