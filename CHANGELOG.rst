.. _changelog_f:

==========
Changelog
==========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

1.2.2-SNAPSHOT (2020-11-29)
---------------------------

**Added**

* Support for deploying the documentation on Github Pages. By default the Documentation is pushed to the gh-pages branch.
  Simply enable Github pages (repository settings) with the gh-pages branch and your documentation will build on ``https://username.github.io/repositoryname``


* Inform user during project creation, that GitHub repo creation is highly recommended to use all features of cookietemple

* Fixed a bug that caused the upgrade command to print the wrong information if the local version of cookietemple was a SNAPSHOT version

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
