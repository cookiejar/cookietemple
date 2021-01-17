Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   {% if (cookiecutter.language == 'python') and (cookiecutter.domain == 'cli') -%}reference{% endif %}
   authors
   changelog
   code_of_conduct

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
