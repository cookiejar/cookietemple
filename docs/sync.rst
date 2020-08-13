.. _sync:

=======================
Syncing your project
=======================

Syncing is supposed to integrate any changes to the cookietemple templates back into your already existing project.

Overview
----------

When ``cookietemple sync`` is invoked, cookietemple checks whether a new version of the corresponding template for the current project is available.
If so, cookietemple now creates a temporary project with the most recent template and pushes it to the ``TEMPLATE`` branch.
Next, a pull request is submitted to the ``development`` or most recently used branch.
The syncing process is configurable by setting the desired lower syncing boundary level and blacklisting files from syncing (see :ref:`sync_config`.

Requirements for sync
------------------------

For syncing to work properly, your project has to satisfy a few things:

 1.) A Github repository with your projects code (private or public, organization or non-organization repository).

 2.) An unmodified ``.cookietemple.yml`` file (if you modified this file, what you should never do, syncing may not be able to recreate the project with the most recent template.

 3.) A running, unmodified workflow called :code:`sync.yml`. Modifying this workflow should never be done and results in undefined sync behaviour.

 4.) An active repository secret called :code:`CT_SYNC_TOKEN` for your project's repository containing the encrypted personal access token with at least :code:`repo` scope.

 5.) It is strongly advised not to touch the ``TEMPLATE`` branch.

Configuring sync
-----------------------

.. _sync_config:

Sync level
++++++++++++

Since cookietemple strongly adheres to semantic versioning our templates do too.
Hence, it is customizable whether only major, minor or all (=patch level) releases of the template should trigger cookietemple sync.
The sync level therefore specifies a lower boundary. It can be configured in the::

    [sync_level]
    ct_sync_level = minor

section.

Blacklisting files
++++++++++++++++++++++

Although, cookietemple only submits pull requests for files, which are part of the template sometimes even those files should be ignored.
Examples could be any html files, which at some point contain only custom content and should not be synced.
When syncing, cookietemple examines the ``cookietemple.cfg`` file and ignores any file patterns (e.g. ``*.html``) below the ``[sync_files_blacklisted]`` section.
