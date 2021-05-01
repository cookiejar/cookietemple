.. highlight:: shell

============
Installation
============


Stable release
----------------

| Stable releases are only found on the release page of this Github repository.
| Binaries, are distributed for Linux, MacOS and Windows.


Nightly release
-------------------

| After every push a Github Actions workflows is triggered, which automatically deploys the binaries of the current version as Github artifacts.
| Visit the Github actions page and download any of the recently published artifacts.


From sources
------------

The sources for {{ cookiecutter.project_name }} can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master

Once you have a copy of the source, you can build it with:

.. code-block:: console

    $ ./gradlew build

A platform dependent binary will be build and available in `/build/native-image`.


.. _Github repo: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
.. _tarball: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master
