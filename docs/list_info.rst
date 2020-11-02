.. _list_info:

=============================================
Getting information about available templates
=============================================

Although, information on all cookietemple templates is provided in :ref:`available_templates` in our documentation, it is often times more convenient to get a quick overview from the commandline.
Hence, cookietemple provides two commands ``list`` and ``info``, which print information on all available templates with different levels of detail.

list
-----

``cookietemple list`` is restricted to the short descriptions of the templates. If you want to read more about a specific (sets of) template, please use the :ref:`info_f` command.

.. figure:: images/list_example.png
   :scale: 100 %
   :alt: List example

   Example output of :code:`cookietemple list`. Note that the content of the output is of course subject to change.

Usage
~~~~~~~

cookietemple list can be invoked *via*

.. code-block:: console

    $ cookietemple list

.. _info_f:

info
------

The ``info`` command should be used when the short description of a template is not sufficient and a more detailed description of a specific template is required.

.. figure:: images/info_example.png
   :scale: 100 %
   :alt: Info example

   Example output of ``cookietemple info``.

Usage
~~~~~~~

Invoke :code:`cookietemple info` *via*

.. code-block:: console

    $ cookietemple info <HANDLE/LANGUAGE/DOMAIN>

- ``HANDLE``: a cookietemple template handle such as ``cli-python``.

- ``DOMAIN``: a domain for which cookietemple provides templates for. Example: ``cli``.

- ``LANGUAGE``: A programming language for which cookietemple provides templates for. Example: ``python``.

