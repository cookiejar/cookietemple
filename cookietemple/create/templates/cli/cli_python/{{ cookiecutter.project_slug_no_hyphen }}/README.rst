{{ cookiecutter.project_name }}
===========================

|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
   :target: https://pypi.org/project/{{ cookiecutter.project_slug }}/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/{{cookiecutter.project_slug }}
   :target: https://pypi.org/project/{{ cookiecutter.project_slug }}
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
   :target: https://opensource.org/licenses/{{ cookiecutter.license }}
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/{{ cookiecutter.project_slug }}/latest.svg?label=Read%20the%20Docs
   :target: https://{{ cookiecutter.project_slug }}.readthedocs.io/
   :alt: Read the documentation at https://{{ cookiecutter.project_slug }}.readthedocs.io/
.. |Build| image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20{{ cookiecutter.project_slug }}%20Package/badge.svg
   :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions?workflow=Package
   :alt: Build Package Status
.. |Tests| image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20{{ cookiecutter.project_slug }}%20Tests/badge.svg
   :target: https://github.com/{{ cookiecutter.github_username}}/{{cookiecutter.project_slug }}/actions?workflow=Tests
   :alt: Run Tests Status
.. |Codecov| image:: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* TODO


Installation
------------

You can install *{{ cookiecutter.project_name }}* via pip_ from PyPI_:

.. code:: console

   $ pip install {{ cookiecutter.project_slug }}


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.


Credits
-------

This package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.

.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _PyPI: https://pypi.org/
.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _pip: https://pip.pypa.io/
.. _Usage: https://{{ cookiecutter.project_slug }}.readthedocs.io/en/latest/usage.html
