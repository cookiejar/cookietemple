#!/usr/bin/env python

"""The setup script."""

import os

import {{ cookiecutter.project_slug_no_hyphen }} as module
from setuptools import find_packages, setup


def walker(base, *paths):
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for f in files:
                    file_list.add(os.path.join(dname, f))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = [{%- if cookiecutter.testing_library == 'pytest' %}'pytest-runner', {%- endif %} ]

test_requirements = [{%- if cookiecutter.testing_library == 'pytest' %}'pytest>=3', {%- endif %} ]

{%- set license_classifiers = {
    'MIT': 'License :: OSI Approved :: MIT License',
    'BSD': 'License :: OSI Approved :: BSD License',
    'ISC': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache2.0': 'License :: OSI Approved :: Apache Software License',
    'GNUv3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Boost': 'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
    'Affero': 'License :: OSI Approved :: GNU Affero General Public License v3',
    'CC0': 'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Eclipse': 'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
    'CCBY': 'License :: Public Domain',
    'CCBYSA': 'License :: Public Domain',
    'WTFPL': 'License :: Public Domain',
    'unlicence': 'License :: Other/Proprietary License',
    'Not open source': 'License :: Other/Proprietary License'
} %}

setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        {%- if cookiecutter.license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.license] }}',
        {%- endif %}
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="{{ cookiecutter.project_short_description }}",
    {%- if 'no' not in cookiecutter.command_line_interface|lower %}
    entry_points={
        'console_scripts': [
            f'{{ cookiecutter.project_slug }}={module.__name__}.server:main',
        ],
    },
    {%- endif %}
    install_requires=requirements,
    {%- if cookiecutter.license in license_classifiers %}
    license="{{ cookiecutter.license }}",
    {%- endif %}
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='{{ cookiecutter.project_slug }}',
    name='{{cookiecutter.project_slug}}',
    packages=find_packages(include=['{{ cookiecutter.project_slug_no_hyphen }}', '{{ cookiecutter.project_slug_no_hyphen }}.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'templates', 'static', 'translations'
        ),
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)
