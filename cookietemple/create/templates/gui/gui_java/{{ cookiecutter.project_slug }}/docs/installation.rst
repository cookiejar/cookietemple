.. highlight:: shell

============
Installation
============


From Sources
--------------

The sources for {{ cookiecutter.project_name }} can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/master

To install {{ cookiecutter.project_name }}, run this command in your terminal:

.. code-block:: console

    $ make install

The installation requires `Maven <https://maven.apache.org/>`_ and Java 11+.
To compile {{ cookiecutter.project_name }} run::

    $ make compile

Moreover, to package {{ cookiecutter.project_name }} with a custom, platform dependent JRE run:

    $ make dist

To finally link all those files together into a single executable and distributable binary run:

    $ make binary

Please note that this functionality requires `COOKIETEMPLE <https://cookietemple.com>`_.

.. _Github repo: https://github.com/cookiejardealer/cookietemple
.. _tarball: https://github.com/cookiejardealer/cookietemple/tarball/master
