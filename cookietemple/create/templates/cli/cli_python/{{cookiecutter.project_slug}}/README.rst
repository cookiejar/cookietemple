{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20{{ cookiecutter.project_slug }}%20Package/badge.svg
        :alt: Github Workflow Build {{ cookiecutter.project_slug }} Status

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20{{ cookiecutter.project_slug }}%20Tox%20Test%20Suite/badge.svg
        :alt: Github Workflow Tests Status

.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
    :alt: Dependabot Enabled


{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}

Features
--------

* TODO

Credits
-------

This package was created with COOKIETEMPLE based on a modified `audreyr/cookiecutter-pypackage`_ project template using Cookiecutter_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
