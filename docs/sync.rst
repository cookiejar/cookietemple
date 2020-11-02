.. _sync:

=======================
Syncing your project
=======================

Syncing is supposed to integrate any changes to the cookietemple templates back into your already existing project.
When ``cookietemple sync`` is invoked, cookietemple checks whether a new version of the corresponding template for the current project is available.
If so, cookietemple creates a temporary project with the most recent template and pushes it to the ``TEMPLATE`` branch.
Next, a pull request is submitted to the ``development`` branch.
The syncing process is configurable by setting the desired lower syncing boundary level and blacklisting files from syncing (see :ref:`sync_config`.

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

Run ``cookietemple sync`` as follows

.. code-block:: console
    :linenos:

    $ cookietemple sync PAT GITHUB_USERNAME PROJECT_DIR

- ``PAT``: a Github personal access token with at least the ``repo`` scope. The ``sync_project.yml`` Github workflow uses the PAT set as a Github secret.

--``GITHUB_USERNAME``: the Github username to submit a pull request from. Must match the supplied PAT.

--``PROJECT_DIR``[PWD]: the path to the ``cookietemple.cfg`` file.

Flags
-------

- ``--set-token``: to set the ``CT_SYNC_SECRET`` to a new PAT. Note that the Github username and the PAT must still match for automatic syncing to work.

- ``check-update``: to manually check whether a new release of a template for an already existing project is available. Automatically called when fully syncing.

Configuring sync
-----------------------

.. _sync_config:

Sync level
~~~~~~~~~~~~~~~~

Since cookietemple strongly adheres to semantic versioning our templates do too.
Hence, it is customizable whether only major, minor or all (=patch level) releases of the template should trigger cookietemple sync.
The sync level therefore specifies a lower boundary. It can be configured in the::

    [sync_level]
    ct_sync_level = minor

section.

Blacklisting files
~~~~~~~~~~~~~~~~~~~~

Although, cookietemple only submits pull requests for files, which are part of the template sometimes even those files should be ignored.
Examples could be any html files, which at some point contain only custom content and should not be synced.
When syncing, cookietemple examines the ``cookietemple.cfg`` file and ignores any file patterns (e.g. ``*.html``) below the ``[sync_files_blacklisted]`` section.
