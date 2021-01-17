.. highlight:: shell

============
Installation
============


Stable release
--------------

To install {{ cookiecutter.project_name }}, run this command in your terminal:

.. code-block:: console

    $ pip install {{ cookiecutter.project_name }}

This is the preferred method to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for {{ cookiecutter.project_name }} can be downloaded from the `Github repo`_.
Please note that you require `poetry`_ to be installed.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make install


.. _Github repo: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}
.. _tarball: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}/tarball/master
.. _poetry: https://python-poetry.org/
