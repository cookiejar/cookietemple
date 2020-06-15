.. highlight:: shell

.. _contributing:

============
Contributing
============

Contributions are welcome and greatly appreciated! Every little bit helps and credit will always be given.
If you have any questions or want to get in touch with the core team feel free to join our `Discord server <https://discord.com/channels/708008788505919599/708008788505919602>`_.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/cookiejar/cookietemple/issues.

If you are reporting a bug, please:

* Use the appropriate issue template.
* Be as detailed as possible. The more time you invest into describing the bug, the more time we save solving them, effectively allowing us to improve cookietemple at a faster pace.
* Be patient. We are passionate, hard workers, but also have demanding full time jobs, which require a lot of our attention.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. We would appreciate it if you quickly commented on the respective issue and write that you are working on this bug, to minimize the chances of two people working on the same task.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. The same rule also applies to features. Please write if you're picking up one of the feature suggestions.

Add Templates
~~~~~~~~~~~~~~~~~

| If you're planning to add a new template to cookietemple we highly suggest that you open an issue using the corresponding template and discuss it first with us.
| :ref:`adding_templates` will guide you through the process of adding new templates to cookietemple.
| Please ensure that you are following all the guidelines and that your template meets the requirements.

Write Documentation
~~~~~~~~~~~~~~~~~~~

cookietemple could always use more documentation, whether as part of the official cookietemple docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue `here <https://github.com/cookiejardealer/cookietemple/issues>`_ .

If you are proposing a feature:

* Use the appropriate GitHub issue
* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `cookietemple` for local development.

1. Fork the `cookietemple` repo on GitHub.
2. Clone your fork locally

.. code-block:: console

    $ git clone git@github.com:your_name_here/cookietemple.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development

.. code-block:: console

    $ mkvirtualenv cookietemple
    $ cd cookietemple/
    $ python setup.py develop

4. Create a branch for local development

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox

.. code-block:: console

    $ flake8 cookietemple tests
    $ tox

To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub

.. code-block:: console

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. | If the pull request adds functionality, the docs should be updated.
   | Put your new functionality into a function with a docstring, and add the feature to the list in README.rst, if it is a major feature.
3. The pull request should work for Python 3.7+ and for PyPy. Check your pull request on Github and verify that all checks and GitHub workflows are passing!
4. Please update the :ref:`changelog_f`.


Tips
----

To run a subset of tests::

$ py.test tests.test_cookietemple
