gui-java
---------

Purpose
^^^^^^^^

| gui-java is a modular `JavaFX <https://openjfx.io/>`_ based template to build cross platform Desktop graphical user interfaces (GUIs).
| It uses `Apache Maven <https://maven.apache.org/>`_ to compile the package and :ref:`warp_f` to distribute binaries containing a Java Runtime Environment (JRE).

Design
^^^^^^^^

| The template follows the `standard Maven directory layout <https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html>`_.
  Therefore, all dependencies are defined in the ``pom.xml`` file, the tool source code is in src/java and the tests in src/test.
| Please be aware that gui-java is a modular Java 11+ project, which requires a few modifications to distribute and build JavaFX applications.
  As a result, binaries are a lot smaller. Assuming that your organization is called ``cookiejardealer``, the file tree looks as follows:

.. code::

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
    ├── .github
    │   ├── dependabot.yml
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request_template.md
    │   ├── release-drafter.yml
    │   └── workflows
    │       ├── compile_package.yml
    │       ├── main_master_branch_protection.yml
    │       ├── publish_docs.yml
    │       ├── release-drafter.yml
    │       ├── run_cookietemple_lint.yml
    │       ├── run_java_linting.yml
    │       ├── run_tests.yml
    │       └── sync_project.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── makefiles
    │   ├── Linux.mk
    │   └── Windows.mk
    ├── pom.xml
    ├── .prettierignore
    ├── README.rst
    ├── .readthedocs.yml
    └── src
        ├── main
        │   ├── java
        │   │   ├── module-info.java
        │   │   └── org
        │   │       └── organization
        │   │           ├── FXMLController.java
        │   │           └── MainApp.java
        │   └── resources
        │       └── org
        │           └── organization
        │               ├── scene.fxml
        │               └── styles.css
        └── test
            └── java
                └── org
                    └── organization
                        ├── SimpleClickableButtonTest.java
                        └── SimpleJUnit5ExampleTest.java



Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `Apache Maven <https://maven.apache.org/>`_ to build and solve dependencies
2. `JavaFX (14) <https://openjfx.io/>`_ to build a graphical user interface
3. `JavaFX Maven plugin <https://github.com/openjfx/javafx-maven-plugin>`_ to build a modular package with a JRE
4. :ref:`warp_f` to create a single, distributable, platform specific binary
5. `JUnit 5 <https://junit.org/junit5/>`_ for unit tests
6. `TestFX <https://github.com/TestFX/TestFX>`_ for JavaFX GUI tests
7. Preconfigured `readthedocs <https://readthedocs.org/>`_
8. Eight Github workflows:

  1. ``build_docs.yml``, which builds the readthedocs documentation.
  2. ``compile_package.yml``, which compiles the gui-java project.
  3. ``run_java_linting.yml``, which runs `checkstyle <https://checkstyle.sourceforge.io/>`_ linting using Google's ruleset.
  4. ``run_tests.yml``, which runs the Unit tests. Note that this workflow is currently disabled, since GUI unittests are not possible using Github Actions.
  5. ``run_codecov``, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  6. ``main_master_branch_protection``: Please read :ref:`pr_master_workflow_docs`.
  7. ``release-drafter.yml``: Please read :ref:`release_drafter_workflow`.  8. ``run_cookietemple_lint.yml``, which runs ``cookietemple lint`` on the project.
  8. ``sync_project.yml``, which syncs the project to the most recent cookietemple template version.

Usage
^^^^^^^^

| The usage of gui-java is primarily Makefile based. Please be aware that you need `Apache Maven <https://maven.apache.org/>`_ and Java 11+ installed.
| All (Maven) commands are wrapped into Make commands, but can of course also be called directly:

The generated gui-java project can be installed using::

    make install

Other make targets include::

    make clean

which removes all build files::

    make dist

which runs jlink to build the gui-java project with a custom platform dependent JRE.
Be aware, that this results in six folders. The executable binary can be found in the target/bin folder and is called ``launcher``.

If you want to package the resulting custom JRE together with the launcher and all other required files (aka the six folders), then run the::

    make binary

goal. ``make binary`` calls the ``make dist`` goal and then packages the files into a single, platform dependent executable using :ref:`warp_f`.
This executable can then be easily distributed.

Tests can be run via::

    make test

All possible Makefile commands can be viewed using::

    make help

FAQ
^^^^^

None yet.
