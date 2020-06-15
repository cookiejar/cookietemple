.. _github_support:

================
Github Support
================

| cookietemple uses `GitPython <https://gitpython.readthedocs.io/en/stable/>`_ and `PyGithub <https://pygithub.readthedocs.io/en/latest/introduction.html>`_ to automatically create a repository, add, commit and push all files.
  Moreover, issue labels and a development branch are created.
| When running :code:`cookietemple create` for the first time, you may be prompted for your Github username, which will be saved locally in :code:`~/cookietemple_conf.cfg`.
  Afterwards, if the answer to "Do you want to create a Github repository and push to it" was "yes", you will be prompted for your Github Personal Access Token.

