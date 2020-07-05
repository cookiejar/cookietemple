#!/usr/bin/env python

"""The setup script."""

import os
import test_sync as module
from setuptools import setup, find_packages


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

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Lukas Heumos",
    author_email='lukas.heumos@posteo.net',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Some fancy sync test",
    entry_points={
        'console_scripts': [
            'test-sync=test_sync.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='test_sync',
    name='test-sync',
    packages=find_packages(include=['test_sync', 'test_sync.*']),
    package_data={
        module.__name__: walker(
            os.path.dirname(module.__file__),
            'files'
        ),
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mlf-core/test_sync',
    version='1.2.1',
    zip_safe=False,
)
