.. _sync:

=======================
Syncing your project
=======================

Syncing is supposed to integrate any changes to the COOKIETEMPLE templates back into your already existing project.
Due to the inherent complexity of this task, it is **not yet implemented**. However, discussions and contributions are very welcome! Please get in touch with us (see :ref:`contributing`).

Our first draft is available `here <https://github.com/cookiejar/cookietemple/issues/175>`_ for discussion.

Requirements for syncing
------------------------
For syncing to work properly, your project has to satisfy a few things:

 1.) A Github repository with your projects code (private or public, orga or non-orga repository).

 2.) An unmodified .cookietemple.yml file (if you modified this file, what you should never do, syncing may fail with strange errors).

 3.) The latest cookietemple release installed on your machine/in your environment (If you enabled dependabot, take a look if any open PRs are available concerning cookietemple).
 Note that any command you run using cookietemple will therefore check if an upgrade is available and inform you about an update, because sync will not run if
 you are using an outdated version of cookietemple.

 4.) A running, unmodified workflow called :code:`check_template_update.yml`. Modifying this workflow should never be done and results in undefined sync behaviour.

 5.) An active repository secret called :code:`CT_SYNC_TOKEN` for your project's repository containing the encrypted personal access token with at least :code:`repo` scope.
