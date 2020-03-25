#!/usr/bin/env python
# -*- coding: utf-8 -*-

'""The setup script.""'
import os

from setuptools import setup, find_packages
from setuptools.command.install import install

import cookietemple as module


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OverrideInstall(install):
    """
    Used to set the file permissions of the Warp executables to 755. Overrides the installation process
    Source: https://stackoverflow.com/questions/5932804/set-file-permissions-in-setup-py-file
    """

    def run(self):
        MODE = 0o755
        install.run(self)  # calling install.run(self) ensures that everything that happened previously still happens, so the installation does not break!

        # Set the permissions to 755 when copying the Warp executables
        for filepath in self.get_outputs():
            executables = filepath.split('/')[-1]
            WARP_EXECUTABLES = ['linux-x64.warp-packer', 'macos-x64.warp-packer', 'windows-x64.warp-packer.exe']
            if executables in WARP_EXECUTABLES:
                print(f'{bcolors.OKBLUE}Changing permissions of {executables} to {oct(MODE)[2:]} ...')
                os.chmod(filepath, MODE)


def walker(base: str, *paths) -> list:
    """
    Used to fetch a list of files below a given directory.
    They are to be packaged with COOKIETEMPLE

    :param base: Base directory to start from
    :param paths: Unpacked directories to return
    :return: List of filenames, which are supposed to be packaged with COOKIETEMPLE
    """
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

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author='Lukas Heumos',
    author_email='lukas.heumos@posteo.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description='A cookiecutter based project template creation tool supporting several domains and languages with linting and template sync support.',
    entry_points={
        'console_scripts': [
            'cookietemple=cookietemple.cookietemple_cli:main',
        ],
    },
    install_requires=requirements,
    license='GNU General Public License v3',
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
    url='https://github.com/zethson/cookietemple',
    version='0.1.0',
    zip_safe=False,
    # cmdclass={'install': OverrideInstall} # This breaks the copying of some files! They seem to be cached or something. Dependencies are also not installed?
)
