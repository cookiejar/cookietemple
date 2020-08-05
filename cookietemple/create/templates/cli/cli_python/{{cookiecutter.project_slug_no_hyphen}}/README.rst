{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20{{ cookiecutter.project_slug }}%20Package/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20{{ cookiecutter.project_slug }}%20Package/badge.svg
        :alt: Github Workflow Build {{ cookiecutter.project_name }} Status

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20{{ cookiecutter.project_slug }}%20Tox%20Test%20Suite/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20{{ cookiecutter.project_slug }}%20Tox%20Test%20Suite/badge.svg
        :alt: Github Workflow Tests Status

.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg
        :target: https://img.shields.io/pypi/v/{{ cookiecutter.project_name }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_name }}

{% if is_open_source %}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_name }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_name }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
        :target: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
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

This package was created with cookietemple_ based on a modified audreyr/cookiecutter-pypackage_ project template using Cookiecutter_.

.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _audreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
