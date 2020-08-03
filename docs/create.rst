.. _create:

================
Create a project
================

| Creating projects from templates is the heart of cookietemple.
| Our templates adhere to best practices and try to be as modern as possible. Furthermore, they try to automate tasks such as automatical dependency resolvement and installation, packaging, deployment and more.
| To learn more about our templates please visit :ref:`available_templates` and check out your template of interest.

The creation of a new project can be invoked by

.. code-block:: console

    $ cookietemple create

which will guide you through the creation process of your (customized) project via prompts. If you do not have a cookietemple config yet, you will be asked to create one first.
The full name, email and possibly more information set during the configuration process is required when creating the project. For more details please visit :ref:`config`.
The prompts follow the pattern of domain (e.g. cli, gui, ...), subdomain (if applicable, e.g. website), language (e.g. Python) followed by template specific prompts (e.g. testing frameworks, ...).
| The template will be created at the current working directory, where cookietemple has been called.

It is also possible to directly create a specific template using its handle

.. code-block:: console

    $ cookietemple create --handle <HANDLE>

| After the template has been created, linting (see :ref:`lint`) is automatically performed to verify that the template creation process was successful.
| You may already be made aware of any TODOs, which you should examine before coding your project.
| Finally, you will be asked whether or not you want to automatically push your new project to Github. For more details about the Github support please visit :ref:`github_support`.
| Note that in order to use the automatic Github repo creation feature, you need to set a personal access token (for login, since a login via password will be deprecated in Autumn 2020) via :code:`cookietemple config pat` (if not already done). This token is also used for cookietemple's sync feature.
| In order to use the sync feature, make sure to tick at least the :code:`repo` scope when creating the token. To use sync even for organisation repos, you will also need to tick the :code:`admin:org` scope.
| Take a look at `the Github docs <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_ to see, how to create a personal access token for your Github account.
