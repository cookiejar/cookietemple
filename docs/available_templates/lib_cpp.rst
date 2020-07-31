lib-cpp
------------

Purpose
^^^^^^^^
A template for modern C++ projects - both executables and libraries - using CMake, Clang-Format, CI, unit testing and more, with support for downstream inclusion.

Design
^^^^^^^^
The template is inspired by several others (mainly `TheLartians' <https://github.com/TheLartians/ModernCppStarter>`_ `and Jason Turner's <https://github.com/lefticus/cpp_starter_project>`). It is using `CMake <https://cmake.org/>`_ as its build system.

.. code ::

   ├── cmake
   │   ├── CompilerWarnings.cmake
   │   ├── Conan.cmake
   │   ├── {{ cookiecutter.project_slug }}Config.cmake.in
   │   ├── Doxygen.cmake
   │   ├── SourcesAndHeaders.cmake
   │   ├── StandardSettings.cmake
   │   ├── StaticAnalyzers.cmake
   │   ├── Utils.cmake
   │   ├── Vcpkg.cmake
   │   └── version.hpp.in
   ├── CMakeLists.txt
   ├── codecov.yaml
   ├── CONTRIBUTING.rst
   ├── Dockerfile
   ├── docs
   │   ├── installation.rst
   │   └── usage.rst
   ├── include
   │   └── {{ cookiecutter.project_slug }}
   │       └── tmp.hpp
   ├── Makefile
   ├── README.rst
   ├── src
   │   └── tmp.cpp
   └── test
       ├── CMakeLists.txt
       └── src
           └── tmp_test.cpp

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Modern **CMake** configuration and project

2. An example of a **Clang-Format** config, inspired from the base
   *Google* model, with minor tweaks.

3. **Static analyzers** integration, with *Clang-Tidy* and *Cppcheck*, the former being the default option

4. **Doxygen** support, through the ``ENABLE_DOXYGEN`` option, which can enable if desired_config

5. **Unit testing** support, through *GoogleTest* (with an option to enable *GoogleMock*) or *Catch2*

6. **Code coverage**, enabled by using the ``ENABLE_CODE_COVERAGE`` option, through *Codecov* CI integration

7. **Package manager support**, with *Conan* and *Vcpkg*, through their respective options

8. **CI workflows for Windows, Linux and MacOS** using *GitHub Actions*, making use of the caching features, to ensure minimum run time

9. Options to build as a header-only library or executable, not just a
   static or shared library

10. **CCache** integration, for speeding up build times

Usage
^^^^^^^^

Installing
++++++++++++++

To install an already built project, you need to run the ``install``
target with CMake. For example:

.. code:: bash

   cmake --build build --target install --config Release

   # a more general syntax for that command is:
   cmake --build <build_directory> --target install --config <desired_config>

Building the project
+++++++++++++++++++++++

To build the project, all you need to do, **after
correctly `installing the project <README.rst#Installing>`_**, is run
a similar **CMake** routine to the the one below:

.. code:: bash

   mkdir build/ && cd build/
   cmake .. -DCMAKE_INSTALL_PREFIX=/absolute/path/to/custom/install/directory
   cmake --build . --target install

..

   **Note:** *The custom* ``CMAKE_INSTALL_PREFIX`` *can be omitted if you
   wish to install in* `the default install
   location <https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html>`_.

More options that you can set for the project can be found in the
`cmake/StandardSettings.cmake
file <cookietemple/create/templates/lib/lib_cpp/{{ cookiecutter.project_slug }}/cmake/StandardSettings.cmake>`_. For certain options additional
configuration may be needed in their respective ``*.cmake`` files (i.e.
Conan needs the ``CONAN_REQUIRES`` and might need the ``CONAN_OPTIONS``
to be setup for it work correctly; the two are set in the
`cmake/Conan.cmake file <cookietemple/create/templates/lib/lib_cpp/{{ cookiecutter.project_slug }}/cmake/Conan.cmake>`_).

Generating the documentation
+++++++++++++++++++++++++++++++++

In order to generate documentation for the project, you need to
configure the build to use Doxygen. This is easily done, by modifying
the workflow shown above as follows:

.. code:: bash

   mkdir build/ && cd build/
   cmake .. -D<project_name>_ENABLE_DOXYGEN=1 -DCMAKE_INSTALL_PREFIX=/absolute/path/to/custom/install/directory
   cmake --build . --target doxygen-docs

..

   **Note:** *This will generate a* ``docs\/`` *directory in
   the **project's root directory**.*

Running tests
+++++++++++++++++++++++

By default, the template uses `Google
Test <https://github.com/google/googletest/>`_ for unit testing. Unit
testing can be disabled in the options, by setting the
``ENABLE_UNIT_TESTING`` (from
`cmake/StandardSettings.cmake <cookietemple/create/templates/lib/lib_cpp/{{ cookiecutter.project_slug }}/cmake/StandardSettings.cmake>`_) to be
false. To run the tests, simply use CTest, from the build directory,
passing the desire configuration for which to run tests for. An example
of this procedure is:

.. code:: bash

   cd build          # if not in the build directory already
   ctest -C Release  # or `ctest -C Debug` or any other configuration you wish to test

   # you can also run tests with the `-VV` flag for a more verbose output (i.e.
   #GoogleTest output as well)

FAQ
^^^^

None yet.
