.. _changelog_f:

==========
Changelog
==========

This project adheres to `Semantic Versioning <https://semver.org/>`_.

1.2.0 (2020-11-22)
------------------

**Added**
linter for cookietemple.cfg file to ensure integrity
a path parameter to create projects on other locations than the CWD

**Fixed**
sync workflow
java templates WFs due to a GithubActions update
default branch creation when creating and pushing a project to GitHub
updated documentation
web template deployment script (refactored) and workflows

**Dependencies**

**Deprecated**
GitHub PAT with only repo scope (needs workflows permissions now too)


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
