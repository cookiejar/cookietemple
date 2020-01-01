#!/usr/bin/env python

"""The setup script."""

import os
from setuptools import setup, find_packages

import {{cookiecutter.project_slug}} as module


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

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="{{cookiecutter.full_name}}",
    author_email='{{cookiecutter.email}}',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="{{cookiecutter.project_short_description}}",
    entry_points={
        'console_scripts': [
            '{{cookiecutter.project_slug}}={}.server:main'.format(module.__name__),
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='{{cookiecutter.project_slug}}',
    name='{{cookiecutter.project_slug}}',
    packages=find_packages(include=['{{cookiecutter.project_slug}}', '{{cookiecutter.project_slug}}.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'templates', 'static', 'translations'
        ),
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}',
    version='{{cookiecutter.version}}',
    zip_safe=False,
)
