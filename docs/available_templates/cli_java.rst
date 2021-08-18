cli-java
---------

Purpose
^^^^^^^^

cli-java is a `Java <https://www.java.com>`_ based template for designed for command line applications, which require a fast startup time.
Hence, it is based on `GraalVM <https://www.graalvm.org/>`_, which allows for the packaging of the application into small, native self-contained executables.
`Picocli <https://picocli.info/>`_ is used as main library for the design of the command line interface.

Design
^^^^^^^^

The template is based on a standard `Maven directory structure <https://www.baeldung.com/maven-directory-structure>`_. However, it is using `Gradle <https://gradle.org/>`_ as build tool.

.. code::

    ├── build.gradle
    ├── CODE_OF_CONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── code_of_conduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── readme.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── .gitattributes
    ├── .github
    │   ├── dependabot.yml
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request_template.md
    │   ├── release-drafter.yml
    │   └── workflows
    │       ├── build_deploy.yml
    │       ├── main_master_branch_protection.yml
    │       ├── publish_docs.yml
    │       ├── release-drafter.yml
    │       ├── run_checkstyle.yml
    │       ├── run_cookietemple_lint.yml
    │       ├── run_tests.yml
    │       └── sync_project.yml
    ├── .gitignore
    ├── gradle
    │   └── wrapper
    │       ├── gradle-wrapper.jar
    │       └── gradle-wrapper.properties
    ├── gradlew
    ├── gradlew.bat
    ├── LICENSE
    ├── Makefile
    ├── makefiles
    │   ├── Linux.mk
    │   └── Windows.mk
    ├── .prettierignore
    ├── .project
    ├── README.rst
    ├── .readthedocs.yml
    ├── .settings
    │   └── org.eclipse.buildship.core.prefs
    ├── settings.gradle
    └── src
        ├── main
        │   └── java
        │       └── com
        │           └── organization
        │               └── Exploding_springfield.java
        └── test
            └── java
                └── com
                    └── organization
                        ├── Exploding_springfieldImageTest.java
                        ├── Exploding_springfieldTest.java
                        └── NativeImageHelper.java


Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `Gradle <https://gradle.org/>`_ as build tool
2. `GraalVM <https://www.graalvm.org/>`_ as main JDK and virtual layer to allow for native binaries
3. `GraalVM Native Image <https://www.graalvm.org/docs/reference-manual/native-image/>`_ to build platform dependent self-contained executables
4. `JUnit 5 <https://junit.org/junit5/>`_ as main testing framework
5. `Picocli <https://picocli.info/>`_ to implement the command line interface
6. Preconfigured `readthedocs <https://readthedocs.org/>`_
7. Seven Github workflows:

  1. ``build_docs.yml``, which builds the Read the Docs documentation.
  2. ``build_deploy.yml``, which builds the cli-java project into Linux, MacOS and Windows executables. They are deployed as build artifacts.
  3. ``run_checkstyle.yml``, which runs `checkstyle <https://checkstyle.sourceforge.io/>`_ linting using Google's ruleset.
  4. ``run_tests.yml``, which runs all JUnit tests.
  5. ``main_master_branch_protection``: Please read :ref:`pr_master_workflow_docs`.
  6. ``release-drafter.yml``: Please read :ref:`release_drafter_workflow`.
  7. ``run_cookietemple_lint.yml``, which runs ``cookietemple lint`` on the project.
  8. ``sync_project.yml``, which syncs the project to the most recent cookietemple template version

Usage
^^^^^^^^

cli-java requires you to have `Gradle <https://gradle.org/>`_, `GraalVM <https://www.graalvm.org/>`_ and
`GraalVM Native Image <https://www.graalvm.org/docs/reference-manual/native-image/>`_ installed.
Please follow the instructions on the respective websites to install them. Ensure that GraalVM is the default JDK by running `java --version`

A platform dependent executable (of the current running operating system!) can then be build by invoking::

    make binary

or alternatively::

    gradle build

Your platform dependent executable can then be found in the folder ``build/native-image``.

Alternatively you can directly build and run your binary by invoking::

    make run

All tests can be run by::

    make test

Other make targets include::

    make clean

which removes all build files::

    make dist

All possible Makefile commands can be viewed using::

    make help

FAQ
^^^^^

Can I use cli-java without GraalVM?
+++++++++++++++++++++++++++++++++++++++++++++++

cli-java is purposefully designed with GraalVM and native images in mind. We advise against using it without GraalVM.

How can I access the build artifacts?
++++++++++++++++++++++++++++++++++++++++++++

Go to the Github Actions tab, select the build_deploy workflow and there you can find the artifacts.
Note that the workflow must have completed successfully for all operating systems.
