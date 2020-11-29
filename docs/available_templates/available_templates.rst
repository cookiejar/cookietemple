.. _available_templates:

=========================
Available templates
=========================

cookietemple currently has the following templates available:

1. `cli-java`_
2. `cli-python`_
3. `gui-java`_
4. `lib-cpp`_
5. `pub-thesis-latex`_
6. `web-website-python`_

In the following every template is devoted its own section, which explains its purpose, design, included frameworks/libraries, usage and frequently asked questions.
A set of frequently questions, which all templates share see here: :ref:`all_templates_faq` FAQ.
It is recommended to use the sidebar to navigate this documentation, since it is very long and cumbersome to scroll through.

.. include:: cli_python.rst
.. include:: cli_java.rst
.. include:: gui_java.rst
.. include:: lib_cpp.rst
.. include:: pub_thesis_latex.rst
.. include:: web_website_python.rst

.. _all_templates_faq:

Shared FAQ
----------------------

How do I publish my documentation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cookietemple ships with a full, production ready `Read the Docs <https://readthedocs.org/>`_ setup and with a complete gh-pages setup.

Read the Docs
+++++++++++++++++

You need to `import your documentation <https://docs.readthedocs.io/en/stable/intro/import-guide.html>`_ on Read the Docs website.
Do not forget to sync your account first to see your repository.
Your documentation will then be available on ``https://repositoryname.readthedocs.io/``

Github Pages
+++++++++++++++

Your documentation is automatically pushed to the ``gh-pages`` branch. Follow the documentation on
``configuring a publishing source for your Github pages site <https://docs.github.com/en/free-pro-team@latest/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>`_
and select the gh-pages branch. Your documentation will then be available on ``https://username.github.io/repositoryname``.

What is Dependabot and how do I set it up?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Dependabot <https://dependabot.com/>`_ is a service, which (for supported languages) automatically submits pull requests for dependency updates.
cookietemple templates ship with dependabot configurations, if the language is supported by Dependabot.
To enable Dependabot you need to login (with your Github account) and add your repository (or enable Dependabot for all repositories).
Note that you need to do this for every organization separately. Dependabot will then pick up the configuration and start submitting pull requests!

How do I add a new template?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please follow :ref:`adding_templates`.
