.. _changelog_f:

==========
Changelog
==========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

1.3.2 (2021-04-17)
------------------

**Added**

**Fixed**

* fixed an issue that caused sync to fail on orga repos

**Dependencies**

**Deprecated**

1.3.1 (2021-04-12)
------------------

**Added**

**Fixed**

* sync will now not happen if a unmerged cookietemple sync PR is still open
* cookietemple lint workflow now uses current cookietemple version, where changes were introduced

**Dependencies**

**Deprecated**



1.3.0 (2021-01-17)
------------------

**Added**

* cli-python version 2.0.0 with Poetry, Nox, pre-commit (with black, prettier, [...]), working module autogeneration and much more.
* [ALL TEMPLATES] Removed Changelog.rst files in favor of Release Drafter, a GitHub Action to automatically include descriptions of changes into a new release

**Fixed**

* blacklisted files for sync defined by the user are now correctly picked up
* blacklisted sync files, that are newly introduced by a PR are now included in the sync PR, they were introduced but not in the following ones

**Dependencies**

**Deprecated**


1.2.4 (2020-12-19)
------------------

**Added**

* refactored sync PR queries using pygithub now instead of requests

**Fixed**

* fixed a bug causing pub template creation to fail and remove the current working directory

**Dependencies**

**Deprecated**


1.2.3 (2020-12-13)
------------------

**Added**

* the sync PR is now always created from a new, temporary sync branch and not from TEMPLATE branch anymore

**Fixed**

* fixed a bug, that causes blacklisted files to be synced
* fixed a bug, where changes made to blacklisted files during sync were not discarded
* fixed a bug, when creating a project with a path parameter named like the project caused a move

**Dependencies**

**Deprecated**


1.2.2 (2020-12-06)
------------------

**Added**

* Support for deploying the documentation on Github Pages. By default the Documentation is pushed to the gh-pages branch.
  Simply enable Github pages (repository settings) with the gh-pages branch and your documentation will build on ``https://username.github.io/repositoryname``
* Inform user during project creation, that GitHub repo creation is highly recommended to use all features of cookietemple
* Fixed a bug that caused the upgrade command to print the wrong information if the local version of cookietemple was a SNAPSHOT version
* Cookietemple's GitHub Actions now print lint and create results colored
* Added requirements.txt and requirements_dev.txt (Python projects) to blacklisted sync files
* Added build.gradle (Cli Java) and pom.xml (GUI Java) to blacklisted sync files
* Updated the config file linter to check whether those files are excluded from sync
* Updated docs with new lint error handling codes

**Fixed**

**Dependencies**

**Deprecated**


1.2.1 (2020-11-22)
------------------

**Added**

**Fixed**

* linting errors URL

**Dependencies**

**Deprecated**


1.2.0 (2020-11-22)
------------------

**Added**

* a linter for cookietemple.cfg file to ensure integrity
* a path parameter to create projects on other locations than the CWD

**Fixed**

* sync workflow (try to create a PR against development or, if none, default branch)
* java templates WFs due to a GithubActions update
* default branch creation when creating and pushing a project to GitHub
* web template deployment script (refactored) and workflows
* updated documentation

**Dependencies**

**Deprecated**

* GitHub PAT with only repo scope (needs workflows permissions now too)


1.0.1 (2020-11-03)
------------------

**Added**

**Fixed**

* cookietemple lint workflow does no longer try to run autopep8 for python projects

**Dependencies**

**Deprecated**


1.0.0 (2020-11-03)
------------------

**Added**

* Documentation hosted on https://cookietemple.readthedocs.io/
* Configuring cookietemple

* Creating templates
* cli-python template
* web-website-python template
* cli-java template
* cli-kotlin template
* gui-java template
* gui-kotlin template
* pub-thesis template

* Linting templates
* Listing templates
* Getting detailed info on templates
* Bumping the version of templates
* Packaging templates using Warp

**Fixed**

**Dependencies**

**Deprecated**
