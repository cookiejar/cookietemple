.. _github_support:

================
Github Support
================

Overview
-------------

cookietemple uses `GitPython <https://gitpython.readthedocs.io/en/stable/>`_ and `PyGithub <https://pygithub.readthedocs.io/en/latest/introduction.html>`_ to automatically create a repository, add, commit and push all files.
Moreover, issue labels, a development and a TEMPLATE branch are created. The TEMPLATE branch is required for :ref:`sync` to work and should not be touched manually.

Branches
--------------

Overview
~~~~~~~~~~~~~~~~

git branches can be understood as diverging copies of the main line of development and facilitate parallel development.
To learn more about branches read `Branches in a Nutshell <https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>`_ of the `Pro Git Book <https://git-scm.com/book>`_.
A simple best practice development workflow follows the pattern that the ``master`` branch always contains the latest released code.
It should only be touched for new releases. Code on the ``master`` branch must compile and be as bug free as possible.
Development takes place on the ``development`` branch. All parallelly developed features eventually make it into this branch.
The ``development`` branch should always compile, but it may contain incomplete features or known bugs.
cookietemple creates a ``TEMPLATE`` branch, which is required for :ref:`sync` to work and should not be touched manually.

Branch protection rules
~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Github Actions
---------------------



Issue labels
----------------

cookietemple's Github support automatically creates `issue labels <https://help.github.com/en/github/managing-your-work-on-github/labeling-issues-and-pull-requests>`_.
Currently the following labels are automatically created:

1. dependabot: All templates, which include `Dependabot <https://dependabot.com/>`_ support label all Dependabot pull requests with this label.
