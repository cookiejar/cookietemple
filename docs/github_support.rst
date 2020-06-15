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

cookietemple sets several branch protection rules, which enforce a minimum standard of best branch practices.
For more information please read `about protected branches <https://help.github.com/en/github/administering-a-repository/about-protected-branches>`_.
The following branch protection rules only apply to the ``master`` branch:

1. Require status checks to pass before merging: The complete CI/CD (see below) pipeline has to pass and requested pull request reviewers have to approve the pull request.
2. Required review for pull requests: A pull request to ``master`` can only be merged if the code was at least reviewed by one person. If you are developing alone you can merge with your administrator powers.
3. Dismiss stale pull request approvals when new commits are pushed.

Github Actions
---------------------

Overview
~~~~~~~~~~~~~~~

Modern development tries to merge new features and bug fixes as soon as possible into the ``development`` branch, since big, diverging branches are more likely to lead to merge conflicts.
This practice is known as `continuous integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ (CI).
Continuous integration is usually complemented with automated tests and continuous delivery (CD).
All of cookietemple's templates feature `Github Actions <https://github.com/features/actions>`_ as main CI/CD service.
Please read the `Github Actions Overview <https://github.com/features/actions>`_ for more information.
On specific conditions (usually push events), the Github Actions workflows are triggered and executed.
The developers should ensure that all workflows always pass before merging, since they ensure that the package still builds and all tests are executed successfully.

.. _pr_master_workflow_docs:

pr_to_master_from_patch_release_only workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All templates feature a workflow called ``pr_to_master_from_patch_release_only.yml``.
This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the ``master`` branch
origins from a branch that does not contain ``PATCH`` or ``release`` in its branch name.
If development code is written on a branch called ``development``and a new release of the project is to be made,
one should create a ``release`` branch only for this purpose and then merge it into ``master`` branch.
This ensures that new developments can already be merged into ``development``, while the release is finally prepared.
The :code:``PATCH`` branch should be used for required :code:`hotfixes` (checked out directly from :code:`master` branch) because, in the meantime, there might
multiple developments going on at ``development`` branch and you dont want to interfere with them.

Issue labels
----------------

cookietemple's Github support automatically creates `issue labels <https://help.github.com/en/github/managing-your-work-on-github/labeling-issues-and-pull-requests>`_.
Currently the following labels are automatically created:
https://en.wikipedia.org/wiki/Continuous_integration
1. dependabot: All templates, which include `Dependabot <https://dependabot.com/>`_ support label all Dependabot pull requests with this label.
