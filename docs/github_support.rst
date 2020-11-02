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

1. Required review for pull requests: A pull request to ``master`` can only be merged if the code was at least reviewed by one person. If you are developing alone you can merge with your administrator powers.
2. Dismiss stale pull request approvals when new commits are pushed.

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All templates feature a workflow called ``pr_to_master_from_patch_release_only.yml``.
This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the ``master`` branch
origins from a branch that does not contain ``PATCH`` or ``release`` in its branch name.
If development code is written on a branch called ``development``and a new release of the project is to be made,
one should create a ``release`` branch only for this purpose and then merge it into ``master`` branch.
This ensures that new developments can already be merged into ``development``, while the release is finally prepared.
The ``PATCH`` branch should be used for required ``hotfixes`` (checked out directly from ``master`` branch) because, in the meantime, there might
multiple developments going on at ``development`` branch and you dont want to interfere with them.

sync_project.yml
~~~~~~~~~~~~~~~~~~~~~~~~~
All templates also feature this workflow. This workflow is used for automatic syncing (if enabled) your project with the latest cookietemple template version.
The workflow is run on push events, although this behavior can be customized if desired.
The workflow calls ``cookietemple sync``, which first checks whether a new template version is available and if so it submits a pull request.
For more details please visit :ref:`sync`.


Secrets
-------
Github secrets are what their name suggests: Encrypted secret values in a repository or an organisation; once they are set their value can be used for sensible data in
a project or an organisation but their raw value can never be seen again even by an administrator (but it can be updated).

Cookietemple uses a secret called :code:`CT_SYNC_TOKEN` for its syncing feature. This secret is automatically created during the repo creation process, if you choose to create a GitHub repo.
The secret contains your encrypted personal access token as its value. Note that this will have no effect on how to login or any other activity in your project.
If you remove the secret or change its value (even with another personal access token of you) the syncing feature will no longer work.
In case you are creating an organisation repository, the secret will also be stored as a repository secret, only usable for your specific project.

See section below in case your Github repo creation failed during the create process.


Error Handling due to failed Github repository creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Errors during the create process due to a failed Github repo creation may occur due to a vast amount of reasons:
Some common error sources are:

1. You have no active internet connection or your firewall protects you against making calls to external APIs.

2. The Github API service or Github itself is unreachable at the moment, which can happen from time to time. In doubt, make sure to check
`the Github status page <https://www.githubstatus.com/>`_.

3. A repo with the same name already exists in your account/your organisation.

Creation fails, ok: But how can I then access the full features of cookietemple?
You can try to fix the issue (or wait some time on case, for example, when Github is down) and then process to create a Github repository manually.
After this, make sure to create a secret named ``CT_SYNC_TOKEN`` with the value of your PAT for your repository. See `the Github docs <https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets>`_
for more information on how to create a secret.

We're planning to provide a command like ``cookietemple config fix-github`` that tries to create a Github repo, set the secret and all other stuff that is going on during the Github repository creation in the create process in a later version.


Issue labels
----------------

cookietemple's Github support automatically creates `issue labels <https://help.github.com/en/github/managing-your-work-on-github/labeling-issues-and-pull-requests>`_.
Currently the following labels are automatically created:
https://en.wikipedia.org/wiki/Continuous_integration
1. dependabot: All templates, which include `Dependabot <https://dependabot.com/>`_ support label all Dependabot pull requests with this label.
