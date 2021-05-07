{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20Linux,%20MacOS,%20Windows%20and%20deploy%20artifacts/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Build%20Linux,%20MacOS,%20Windows%20and%20deploy%20artifacts/badge.svg
        :alt: Github Workflow Build {{ cookiecutter.project_slug }} Status

.. image:: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20Tests/badge.svg
        :target: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/workflows/Run%20Tests/badge.svg
        :alt: Github Workflow Tests Status

{% if is_open_source %}
.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
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

This package was created with cookietemple_ using Cookiecutter_. It is based on a draft by remkop_.

.. _remkop:       https://github.com/remkop
.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
