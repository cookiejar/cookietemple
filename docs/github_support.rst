.. _github_support:

================
Github Support
================

| cookietemple uses `GitPython <https://gitpython.readthedocs.io/en/stable/>`_ and `PyGithub <https://pygithub.readthedocs.io/en/latest/introduction.html>`_ to automatically create a repository, add, commit and push all files.
  Moreover, issue labels and a development branch are created.
| When running :code:`cookietemple create` for the first time, you may be prompted for your Github username, which will be saved locally in :code:`~/cookietemple_conf.cfg`.
  Afterwards, if the answer to "Do you want to create a Github repository and push to it" was "yes", you will be prompted for your Github Personal Access Token.
| Please refer to the `official documentation <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line>`_ on how to create one.
  cookietemple only requires ``repo`` access, so you only need to tick this box.
| cookietemple then encrypts the Personal Access Token, adds the encrypted token to the :code:`cookietemple_conf.cfg` file and saves the key locally in a hidden place. This is safer than Github's official way, which recommends the usage of environment variables or Github Credentials, which both save the token in plaintext.
| If you create a second project using cookietemple at a later stage, you will not be prompted again for your Github username, nor your Personal Access Token. Both information will automatically be extracted and loaded on the fly.

