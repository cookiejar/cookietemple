#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
from setuptools import setup, find_packages

import cookietemple as module


def walker(base: str, *paths) -> list:
    """
    Used to fetch a list of files below a given directory.
    They are to be packaged with cookietemple

    :param base: Base directory to start from
    :param paths: Unpacked directories to return
    :return: List of filenames, which are supposed to be packaged with cookietemple
    """
    file_list = set([])
    cur_dir = os.path.abspath(os.curdir)

    os.chdir(base)
    try:
        for path in paths:
            for dname, dirs, files in os.walk(path):
                for file in files:
                    file_list.add(os.path.join(dname, file))
    finally:
        os.chdir(cur_dir)

    return list(file_list)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author='Lukas Heumos',
    author_email='lukas.heumos@posteo.net',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2 (Apache-2.0)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    description='A cookiecutter based project template creation tool supporting several domains and languages with linting and template sync support.',
    entry_points={
        'console_scripts': [
            'cookietemple=cookietemple.cookietemple_cli:main',
        ],
    },
    install_requires=requirements,
    license='Apache License 2.0',
    long_description=readme,
    include_package_data=True,
    keywords='cookietemple',
    name='cookietemple',
    packages=find_packages(include=['cookietemple', 'cookietemple.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'create/templates', 'package_dist/warp'
        ),
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cookiejar/cookietemple',
    version='1.0.0',
    zip_safe=False,
)
