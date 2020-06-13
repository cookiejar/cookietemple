.. _available_templates:

=========================
Available templates
=========================

COOKIETEMPLE currently has the following templates available:

1. `cli-python`_
2. `cli-java`_
3. `cli-kotlin`_
4. `web-website-python`_
5. `gui-java`_
6. `gui-kotlin`_
7. `pub-thesis-latex`_

In the following every template is devoted its own section, which explains its purpose, design, included frameworks/libraries and usage.

cli-python
----------

Purpose
^^^^^^^^

cli-python is a `Python <https://www.python.org/>`_ based template for designed for command line applications,
but it may also be easily used as standard Python package without any command line interface. It is an improved version of `cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_.

Design
^^^^^^^^

| The Python package is based on a standard `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ structure including a :code:`setup.py`, :code:`setup.cfg`, :code:`MANIFEST.in`,
  :code:`requirements.txt` and :code:`requirements_dev.txt` file.

.. code::

    ├── AUTHORS.rst
    ├── CHANGELOG.rst
    ├── .coafile
    ├── CODEOFCONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── codeofconduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── modules.rst
    │   ├── readme.rst
    │   ├── requirements.txt
    │   └── usage.rst
    ├── .editorconfig
    ├── Exploding_Springfield
    │   ├── cli.py
    │   ├── Exploding_Springfield.py
    │   ├── files
    │   │   └── test.txt
    │   ├── __init__.py
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── build_package.yml
    │       ├── flake8_linting.yml
    │       ├── publish_package.yml
    │       └── tox_testsuite.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── MANIFEST.in
    ├── README.rst
    ├── .readthedocs.yml
    ├── requirements_dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   └── test_Exploding_Springfield.py
    ├── tox.ini
    └── .travis.yml

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ for code packaging
2. `click <https://click.palletsprojects.com/>`_, `argparse <https://docs.python.org/3/library/argparse.html>`_ or no command line interface
3. `pytest <https://docs.pytest.org/en/latest/>`_ or `unittest <https://docs.python.org/3/library/unittest.html>`_ as testing frameworks
4. Preconfigured `tox <https://tox.readthedocs.io/en/latest/>`_ to run pytest matrices with different Python environments
5. Preconfigured `readthedocs <https://readthedocs.org/>`_
6. Eight Github workflows:

  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`build_package.yml`, which builds the cli-python package.
  3. :code:`run_flake8_linting.yml`, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  4. :code:`run_tox_testsuite.yml`, which runs the tox testing suite.
  5. :code:`publish_package.yml`, which publishes the package to PyPi. Note that it only runs on Github release and requires PyPi secrets to be set up.
  6. :code:`run_codecov`, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  7. :code:`run_bandit`, run `bandit <https://github.com/PyCQA/bandit>`_ to discover security issues in your python code
  8. :code:`pr_to_master_from_patch_release_only`: This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the :code:`master` branch
     comes from a branch that does not containd :code:`PATCH` or :code:`release` in its branch name. Why? If you write your development code on a branch called :code:`development`
     and want to make a new release of your project, one should create a :code:`release` branch only for this purpose and then merge it into :code:`master` branch.
     The :code:`PATCH` branch should be used for required :code:`hotfixes` (checked out directly from :code:`master` branch) because, in the meantime, there might
     multiple developments going on at :code:`development` branch and you dont want to interfere with them.


We highly recommend to use click (if commandline interface is required) together with pytest.

Usage
^^^^^^^^

The generated cli-python project can be installed using::

    make install

or alternatively::

    python setup.py install

Your package is then installed globally (or in your virtual environment) on your machine and can be called from your favorite shell::

    <<your_project_name>>

Other make targets include::

    make clean

which removes all build files::

    make dist

which builds source and wheel packages, which can then be used for a PyPi release using

    make release

All possible Makefile commands can be viewed using::

    make help

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

    ├── AUTHORS.rst
    ├── build.gradle
    ├── CHANGELOG.rst
    ├── CODE_OF_CONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── codeofconduct.rst
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
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request_template.md
    │   └── workflows
    │       ├── build_deploy.yml
    │       ├── pr_to_master_from_patch_release_only.yml
    │       ├── run_checkstyle.yml
    │       └── run_tests.yml
    ├── .gitignore
    ├── gradle
    │   └── wrapper
    │       ├── gradle-wrapper.jar
    │       └── gradle-wrapper.properties
    ├── gradlew
    ├── gradlew.bat
    ├── LICENSE
    ├── Makefile
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
5. Preconfigured `readthedocs <https://readthedocs.org/>`_
6. Five Github workflows:

  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`build_deploy.yml`, which builds the cli-java project into Linux, MacOS and Windows executables. They are deployed as build artifacts.
  3. :code:`run_checkstyle.yml`, which runs `checkstyle <https://checkstyle.sourceforge.io/>`_ linting using Google's ruleset.
  4. :code:`run_tests.yml`, which runs all JUnit tests.
  5. :code:`pr_to_master_from_patch_release_only`: This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the :code:`master` branch
     comes from a branch that does not containd :code:`PATCH` or :code:`release` in its branch name. Why? If you write your development code on a branch called :code:`development`
     and want to make a new release of your project, one should create a :code:`release` branch only for this purpose and then merge it into :code:`master` branch.
     The :code:`PATCH` branch should be used for required :code:`hotfixes` (checked out directly from :code:`master` branch) because, in the meantime, there might
     multiple developments going on at :code:`development` branch and you dont want to interfere with them.

Usage
^^^^^^^^

cli-java requires you to have `Gradle <https://gradle.org/>`_, `GraalVM <https://www.graalvm.org/>`_ and
`GraalVM Native Image <https://www.graalvm.org/docs/reference-manual/native-image/>`_ installed.
Please follow the instructions on the respective websites to install them. Ensure that GraalVM is the default JDK by running `java --version`

A platform dependent (of the current running operating system!) can then be build by invoking::

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

cli-kotlin
------------

Purpose
^^^^^^^^

Design
^^^^^^^^

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usage
^^^^^^^^

web-website-python
-------------------

Purpose
^^^^^^^^

This template is a `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_  based Web Template that can be customized from two basic layouts and many available frontend templates.
It contains all the code, necessary for project setup and automatic deployment on a Linux server. It also provides a GitHub Workflow for automatic CSS linting on push using
`Stylelint <https://stylelint.io/>`_.

Design
^^^^^^^^
The whole template is designed to be as customizable as possible. Note that all templates could be customized
with a full featured Frontend template setup during the template creation process. However, if you don´t like the offered templates or simply want to create your own frontend,
you can create your template with only a minimal frontend.
You can choose from two main options:

The basic setup
++++++++++++++++++++++++++++++++++
The basic theme is designed to provide only minimal code needed for getting started: Thus it comes
with only minimal HTML/CSS/JS code (but you can initalize it with a full featured frontend, if you want to) and basic Flask configuration.
However, it contains all the code needed for automatic deployment on a Linux server and adheres to the COOKIETEMPLE project structure standards.
See :ref:`web usage` for more information.

.. code::

    ├── AUTHORS.rst
    ├── CHANGELOG.rst
    ├── .coafile
    ├── CODEOFCONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── codeofconduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── modules.rst
    │   ├── readme.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── Exploding_Springfield
    │   ├── cli.py
    │   ├── Exploding_Springfield.py
    │   ├── files
    │   │   └── test.txt
    │   └── __init__.py
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── build_package.yml
    │       ├── flake8_linting.yml
    │       ├── pr_to_master_from_dev_only.yml
    │       ├── publish_package.yml
    │       └── tox_testsuite.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── MANIFEST.in
    ├── README.rst
    ├── .readthedocs.yml
    ├── requirements_dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   └── test_Exploding_Springfield.py
    ├── tox.ini
    └── .travis.yml


The advanced setup
++++++++++++++++++++++++++++++++++
The advanced theme comes with a lot more functionality by default (and can also be initialized with a full featured, nice frontend):

1. It uses `FlaskSQL-Alchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_ and `FlaskMigrate <https://flask-migrate.readthedocs.io/en/latest/>`_ to setup a `SQLite <https://www.sqlite.org/index.html>`_ application for simple User Login.

2. It provides translation for German and English using `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_.
3. It provides sending mail through `Flask-Mail <https://pythonhosted.org/Flask-Mail/>`_.
4. It provides error handling through custom error pages.
5. Its configured to be automatically deployed in seconds on a Linux server.
6. More is WIP (Contributions are welcome).

.. code::

    ├── AUTHORS.rst
    ├── babel.cfg
    ├── CHANGELOG.rst
    ├── CODEOFCONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── deployment_scripts
    │   ├── Exploding_Springfield
    │   ├── Exploding_Springfield.service
    │   ├── README.md
    │   └── setup.sh
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── conf.py
    │   ├── contributing.rst
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
    ├── Exploding_Springfield
    │   ├── app.py
    │   ├── auth
    │   │   ├── forms
    │   │   │   ├── __init__.py
    │   │   │   ├── login_form.py
    │   │   │   └── register_form.py
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── config.py
    │   ├── errors
    │   │   ├── handlers.py
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── models
    │   │   ├── __init__.py
    │   │   └── users.py
    │   ├── server.py
    │   ├── services
    │   │   └── __init__.py
    │   ├── static
    │   │   ├── assets
    │   │   │   ├── css
    │   │   │   │   └── min_css.css
    │   │   │   ├── images
    │   │   │   │   └── gitkeep
    │   │   │   ├── js
    │   │   │   │   └── min_jss.js
    │   │   │   ├── sass
    │   │   │   │   ├── base
    │   │   │   │   │   └── gitkeep
    │   │   │   │   ├── components
    │   │   │   │   │   └── gitkeep
    │   │   │   │   ├── layout
    │   │   │   │   │   └── gitkeep
    │   │   │   │   └── libs
    │   │   │   │       └── gitkeep
    │   │   │   └── webfonts
    │   │   │       └── gitkeep
    │   │   └── mail_stub.conf
    │   ├── templates
    │   │   ├── auth
    │   │   │   ├── login.html
    │   │   │   └── register.html
    │   │   ├── base.html
    │   │   ├── errors
    │   │   │   ├── 400.html
    │   │   │   ├── 403.html
    │   │   │   ├── 404.html
    │   │   │   ├── 410.html
    │   │   │   ├── 500.html
    │   │   │   └── error_template.html
    │   │   └── index.html
    │   └── translations
    │       └── de
    │           └── LC_MESSAGES
    │               ├── messages.mo
    │               └── messages.po
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── build_package.yml
    │       ├── css_lint.yml
    │       ├── flake8_linting.yml
    │       ├── pr_to_master_from_dev_only.yml
    │       └── tox_testsuite.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── MANIFEST.in
    ├── README.rst
    ├── .readthedocs.yml
    ├── requirements_dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    ├── .stylelintrc.json
    ├── tests
    │   ├── __init__.py
    │   └── test_Exploding_Springfield.py
    ├── tox.ini
    └── .travis.yml


Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Both templates are based on `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_ and, in the case of the advanced layout,
make heavy use of its extensions.

1. `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_
2. `click <https://click.palletsprojects.com/>`_, `argparse <https://docs.python.org/3/library/argparse.html>`_ or no command line interface
3. `pytest <https://docs.pytest.org/en/latest/>`_ or `unittest <https://docs.python.org/3/library/unittest.html>`_ as testing frameworks
4. Preconfigured `tox <https://tox.readthedocs.io/en/latest/>`_ to run pytest matrices with different Python environments
5. Preconfigured `readthedocs <https://readthedocs.org/>`_
6. Eight Github workflows:

  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`build_package.yml`, which builds the web-template package.
  3. :code:`run_flake8_linting.yml`, which runs `flake8 <https://flake8.pycqa.org/en/latest/>`_ linting.
  4. :code:`run_tox_testsuite.yml`, which runs the tox testing suite.
  5. :code:`run_css_lint.yml`, which runs `Stylelint <https://stylelint.io/>`_ CSS linting.
  6. :code:`run_codecov`, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  7. :code:`run_bandit`, run `bandit <https://github.com/PyCQA/bandit>`_ to discover security issues in your python code
  8. :code:`pr_to_master_from_patch_release_only`: This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the :code:`master` branch
     comes from a branch that does not containd :code:`PATCH` or :code:`release` in its branch name. Why? If you write your development code on a branch called :code:`development`
     and want to make a new release of your project, one should create a :code:`release` branch only for this purpose and then merge it into :code:`master` branch.
     The :code:`PATCH` branch should be used for required :code:`hotfixes` (checked out directly from :code:`master` branch) because, in the meantime, there might
     multiple developments going on at :code:`development` branch and you dont want to interfere with them.


We highly recommend to use click (if commandline interface is required) together with pytest.

The advanced template therefore uses some more packages including:

1. `FlaskSQL-Alchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_
2. `Flask-Migrate <https://flask-migrate.readthedocs.io/en/latest/>`_
3. `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_ for translations
4. `Flask-Mail <https://pythonhosted.org/Flask-Mail/>`_ for mail
5. `Flask-Bootstrap <https://pythonhosted.org/Flask-Bootstrap/>`_ for basic login page styling
6. `Flask-Login <https://flask-login.readthedocs.io/en/latest/>`_ for login session management
7. `Flask-wtf <https://flask-wtf.readthedocs.io/en/stable/>`_ for the login forms

.. _web usage:

Usage
^^^^^^^^

The basic template usage
++++++++++++++++++++++++++++++++++

The generated flask web project can be installed using::

    $ make install

or alternatively::

    $ python setup.py install

Your package is then installed globally (or in your virtual environment) on your machine and can be called from your favorite shell::

    $ <<your_project_name>>

Other make targets include::

    $ make clean

which removes all build files::

    $ make dist

which builds source and wheel packages, which can then be used for a PyPi release using::

    $ make release

All possible Makefile commands can be viewed using::

    $ make help

Another possibility is to simply run::

    $ export FLASK_APP = path/to/your/app.py
    $ flask run

Note that, if your current directory contains your app.py file, you do not need to set the environment variable lika above!

.. role:: bash(code)
   :language: bash

The advanced template usage
++++++++++++++++++++++++++++++++++
Using the advanced template, you have to consider a few more steps in order to make it work properly:

1. You can install the project just like described above via :bash:`$ make install`.

2. Now, you have to setup and initialize your SQLite database file using :bash:`$ make init_db`. This step is needed otherwise your app won't work!

3. In order to make your translations working, we need to update and compile the recent translations
   Therefore :bash:`$ flask translate update` and then :bash:`$ flask translate compile`. Note that you have to :bash:`$ export FLASK_APP=your/path/to/app.py`
   if not already done. Then, again, run :bash:`$ make install` to pick up your translations into your actual build.

3. Now, fire up :bash:`$ <<your_project_name>>` and see your project setup working.

A quick note on translations: Your advanced template comes with a basic translation setup for German and English translation.
As your project grows, you may need to add new translations. This can be easily done using the provided cli-commands by the template:

1. If you want to add a new language: Use :bash:`$ flask translate init <<my_new_language>>`. Note that my new language must be a valid language literal like
:bash:`en` for english.

2. :bash:`$ flask translate update` to update all language repositories

3. Now you can update your translations in :bash:`your/path/to/translations/yourlanguage/LC_MESSAGES/messages.po`.

3. :bash:`$ flask translate compile` to compile all language repositories

Note that you need to run :bash:`$ make install` each time after updating and compiling your new translations in order for them to take effect. However, this is not
necessary, if you start your application via :bash:`$ flask run`.


Automatic Deployment
^^^^^^^^^^^^^^^^^^^^

Both templates are ready for deployment using nginx and gunicorn and are therefore shipped with a setup script :bash:`path/to/your/project/deployment_scripts/setup.sh`.
There are a few requirements needed in order to deploy:

 1. You need a registered Domain from your preferred DNS-Provider like `Namecheap <https://www.namecheap.com/>`_.
 2. You need a Linux server, like a droplet at `DigitalOcean <https://www.digitalocean.com/>`_, in order to deploy your application.
 3. To start deployment, you have to setup your server initially. You can follow, for example, the steps `here <https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04>`_
    in order to correctly setup your server.

If you meet all the requirements above login (for example via :bash:`$ ssh yourvmusername@your-servers-IP`) into your server and start the setup script::

    $ sudo bash <<your_project_name>>/deployment_scripts/setup.sh

If everything went fine, you should now be able to access your application at your domain.
TODO: IM NGINX.conf is atm a duplicate listen port 80. FIX IT?!
Note that the setup process also includes HTTP to HTTPS redirecting.

If you encounter any problems, dont hesitate to drop us a message in our `Discord <https://discord.com/channels/708008788505919599/708008788505919602>`_. or create an issue `at our github repo <https://github.com/cookiejar/cookietemple/issues/new/choose>`_

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

: code::

    ├── AUTHORS.rst
    ├── CHANGELOG.rst
    ├── CODEOFCONDUCT.rst
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── .dependabot
    │   └── config.yml
    ├── Dockerfile
    ├── docs
    │   ├── authors.rst
    │   ├── changelog.rst
    │   ├── codeofconduct.rst
    │   ├── conf.py
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── make.bat
    │   ├── Makefile
    │   ├── __pycache__
    │   │   └── conf.cpython-38.pyc
    │   ├── readme.rst
    │   ├── requirements.txt
    │   ├── _static
    │   │   └── custom_cookietemple.css
    │   └── usage.rst
    ├── .editorconfig
    ├── .github
    │   ├── ISSUE_TEMPLATE
    │   │   ├── bug_report.md
    │   │   ├── feature_request.md
    │   │   └── general_question.md
    │   ├── pull_request_template.md
    │   └── workflows
    │       ├── build_docs.yml
    │       ├── compile_package.yml
    │       ├── java_linting.yml
    │       └── run_tests.yml
    ├── .gitignore
    ├── LICENSE
    ├── Makefile
    ├── pom.xml
    ├── README.rst
    ├── .readthedocs.yml
    └── src
        ├── main
        │   ├── java
        │   │   ├── module-info.java
        │   │   └── org
        │   │       └── cookiejar
        │   │           ├── FXMLController.java
        │   │           └── MainApp.java
        │   └── resources
        │       └── org
        │           └── cookiejar
        │               ├── scene.fxml
        │               └── styles.css
        └── test
            └── java
                └── org
                    └── cookiejar
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
8. Six Github workflows:

  1. :code:`build_docs.yml`, which builds the readthedocs documentation.
  2. :code:`compile_package.yml`, which compiles the gui-java project.
  3. :code:`run_java_linting.yml`, which runs `checkstyle <https://checkstyle.sourceforge.io/>`_ linting using Google's ruleset.
  4. :code:`run_tests.yml`, which runs the Unit tests. Note that this workflow is currently disabled, since GUI unittests are not possible using Github Actions.
  5. :code:`run_codecov`, apply codecov to your project/PRs in your project and create automatically a report with the details at `codecov.io <https://codecov.io>`_
  6. :code:`pr_to_master_from_patch_release_only`: This workflow runs everytime a PR to your projects master branch is created. It fails, if the PR to the :code:`master` branch
     comes from a branch that does not containd :code:`PATCH` or :code:`release` in its branch name. Why? If you write your development code on a branch called :code:`development`
     and want to make a new release of your project, one should create a :code:`release` branch only for this purpose and then merge it into :code:`master` branch.
     The :code:`PATCH` branch should be used for required :code:`hotfixes` (checked out directly from :code:`master` branch) because, in the meantime, there might
     multiple developments going on at :code:`development` branch and you dont want to interfere with them.

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

gui-kotlin
-------------

Purpose
^^^^^^^^

Design
^^^^^^^^

Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Usage
^^^^^^^^

pub-thesis-latex
--------------------

Purpose
^^^^^^^^

| pub-thesis is a latex based template designed for University theses. It is especially suited for Bachelor-, Master theses and dissertations.
| The `CUED <https://github.com/kks32/phd-thesis-template>`_ PhD thesis template served as basis for this template.

Design
^^^^^^^^

| pub-thesis is a modular latex template, which is reflected in the folder structure. The main tex files are :code:`thesis.tex` and :code:`thesis-info.tex`.
| :code:`thesis-info.tex` mostly defines general information such as name, degree, university etc and :code:`thesis.tex` includes all other tex files such as abstracts, chapters etc.
| The tex files for these chapters are found in their respective subfolders.
| All figures go inside the :code:`Figs` subfolder and all references should be included in :code:`References/references.bib`.

.. code::

    ├── Abstract
    │   └── abstract.tex
    ├── Acknowledgement
    │   └── acknowledgement.tex
    ├── Appendix1
    │   └── appendix1.tex
    ├── Chapter1
    │   └── chapter1.tex
    ├── Chapter2
    │   ├── chapter2.tex
    │   └── Figs
    │       ├── Raster
    │       │   ├── minion.png
    │       │   ├── TomandJerry.png
    │       │   └── WallE.png
    │       └── Vector
    │           ├── minion.eps
    │           ├── TomandJerry.eps
    │           └── WallE.eps
    ├── Chapter3
    │   └── chapter3.tex
    ├── compile-thesis.sh
    ├── compile-thesis-windows.bat
    ├── cookietemple.cfg
    ├── .cookietemple.yml
    ├── Declaration
    │   └── declaration.tex
    ├── Dedication
    │   └── dedication.tex
    ├── Dockerfile
    ├── Figs
    │   ├── CollegeShields
    │   │   ├── Downing.eps
    │   │   ├── Downing.pdf
    │   │   ├── Fitzwilliam.eps
    │   │   ├── Fitzwilliam.pdf
    │   │   ├── FitzwilliamRed.eps
    │   │   ├── FitzwilliamRed.pdf
    │   │   ├── Gonville_and_Caius.jpg
    │   │   ├── Kings.eps
    │   │   ├── Kings.pdf
    │   │   ├── Licenses.md
    │   │   ├── Peterhouse.pdf
    │   │   ├── Queens.eps
    │   │   ├── Queens.pdf
    │   │   ├── src
    │   │   │   ├── Downing.svg
    │   │   │   ├── Kings.svg
    │   │   │   ├── Peterhouse.svg
    │   │   │   ├── Queens.svg
    │   │   │   └── Trinity.svg
    │   │   ├── StJohns.eps
    │   │   ├── StJohns.pdf
    │   │   ├── Trinity.eps
    │   │   └── Trinity.pdf
    │   ├── University_Crest.eps
    │   ├── University_Crest_Long.eps
    │   ├── University_Crest_Long.pdf
    │   └── University_Crest.pdf
    ├── .github
    │   └── workflows
    │       └── build_thesis.yml
    ├── .gitignore
    ├── glyphtounicode.tex
    ├── hooks
    │   ├── install.sh
    │   └── pre-commit
    ├── LICENSE
    ├── Makefile
    ├── PhDThesisPSnPDF.cls
    ├── Preamble
    │   └── preamble.tex
    ├── README.rst
    ├── References
    │   └── references.bib
    ├── sty
    │   └── breakurl.sty
    ├── thesis-info.tex
    ├── thesis.pdf
    ├── thesis.ps
    ├── thesis.tex
    └── Variables.ini


Included frameworks/libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. LaTeX, XeLaTeX and LuaLaTeX support
2. Draft mode: Draft water mark, timestamp, version numbering and line numbering
3. `Bibtex <http://www.bibtex.org/Using/>`_ support
4. A Github workflow :code:`build_thesis.yml`, which builds your thesis in a Docker container

Usage
^^^^^^^^

Building your thesis - LaTeX / PDFLaTeX
+++++++++++++++++++++++++++++++++++++++++

Using latexmk (Unix/Linux/Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template supports ``latexmk``. To generate DVI, PS and PDF run

::

    latexmk -dvi -ps -pdf thesis.tex

Using the make file (Unix/Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The template supports PDF, DVI and PS formats. All three formats can be
generated with the provided ``Makefile``.

To build the ``PDF`` version of your thesis, run:

::

    make

This build procedure uses ``pdflatex`` with ``bibtex`` and will produce
``thesis.pdf``. To use ``pdflatex`` with ``biblatex``, you should run:

::

    make BIB_STRATEGY=biblatex

To use ``XeLaTeX``, you should run:

::

    make BUILD_STRATEGY=xelatex

or with ``biblatex``

::

    make BUILD_STRATEGY=xelatex BIB_STRATEGY=biblatex

To use ``LuaLaTeX``, you should run:

::

    make BUILD_STRATEGY=lualatex

or with ``biblatex``

::

    make BUILD_STRATEGY=lualatex BIB_STRATEGY=biblatex

To produce ``DVI`` and ``PS`` versions of your document, you should run:

::

    make BUILD_STRATEGY=latex

This will use the ``latex`` command to build the document and will
produce ``thesis.dvi``, ``thesis.ps`` and ``thesis.pdf`` documents. You
will need psutils installed

Clean unwanted files

To clean unwanted clutter (all LaTeX auto-generated files), run:

::

    make clean

**Note**: the ``Makefile`` itself is take from and maintained at
`here <http://code.google.com/p/latex-makefile/>`__.

Shell script for PDFLaTeX (Unix/Linux)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage: ``sh ./compile-thesis.sh [OPTIONS] [filename]``

[option] compile: Compiles the PhD Thesis

[option] clean: removes temporary files - no filename required

Using the batch file on Windows OS (PDFLaTeX)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Open command prompt and navigate to the directory with the tex file.
   Run:

   ``compile-thesis-windows.bat``.

-  Alternatively, double click on ``compile-thesis-windows.bat``

Building your thesis - XeLaTeX
++++++++++++++++++++++++++++++++++

Using latexmk (Unix/Linux/Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template supports ``XeLaTeX`` compilation chain. To generate PDF
run

::

    latexmk -xelatex thesis.tex
    makeindex thesis.nlo -s nomencl.ist -o thesis.nls
    latexmk -xelatex -g thesis.tex

Building your thesis - LuaLaTeX
++++++++++++++++++++++++++++++++++

Using latexmk (Unix/Linux/Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This template supports ``LuaLaTeX`` compilation chain. To generate PDF
run

::

    latexmk -pdflatex=lualatex -pdf thesis.tex

Usage details
+++++++++++++++

Thesis information such as title, author, year, degree, etc., and other
meta-data can be modified in ``thesis-info.tex``

Class options
~~~~~~~~~~~~~

The class file, ``PhDThesisPSnPDF``, is based on the standard ``book``
class

It supports the following custom options in the documentclass in
thesis.tex:

(Usage ``\documentclass[a4paper,11pt,print]{PhDThesisPSnPDF}``)

-  ``a4paper`` (default as per the University guidelines) or
   ``a5paper``: Paper size

-  ``11pt`` or ``12pt``: The University of Cambridge guidelines
   recommend using a minimum font size of 11pt (12pt is preferred) and
   10pt for footnotes. This template also supports ``10pt``.

-  ``oneside`` or ``twoside`` (default): This is especially useful for
   printing double side (twoside) or single side.

-  ``print``: Supports Print and Online Version with different page
   margins and hyperlink styles. Use ``print`` in the options to
   activate Print Version with appropriate margins and page layout and
   view styles. Leaving the options field blank will activate Online
   version.

-  ``custommargin``: You can alter the margin dimension for both print
   and online version by using the keyword ``custommargin`` in the
   options. Then you can define the dimensions of the margin in the
   ``preamble.tex`` file:

   ::

       \ifsetCustomMargin
         \RequirePackage[left=37mm,right=30mm,top=35mm,bottom=30mm]{geometry}
         \setFancyHdr
       \fi

   ``\setFancyHdr`` should be called when using custom margins for
   proper header/footer dimensions

   ``\ifsetMargin`` is deprecated, please use ``\ifsetCustomMargin``
   instead.

-  ``index``: Including this option builds the index, which is placed at
   the end of the thesis.

   Instructions on how to use the index can be found
   `here <http://en.wikibooks.org/wiki/LaTeX/Indexing#Using_makeidx>`__.

   *Note*: the package ``makeidx`` is used to create the index.

-  ``abstract``: This option enables only the thesis title page and the
   abstract with title and author to be printed.

-  ``chapter``: This option enables only the specified chapter and it's
   references. Useful for review and corrections.

-  ``draft``: The default draft mode supports some special features such
   as line numbers, images, and water mark with timestamp and custom
   text. Position of the text can be modified in ``preamble.tex``.

-  ``draftclassic``: This mode is similar to the default draft mode in
   the book class. Images are not loaded.

-  ``lineno``: Enables pagewise line numbering on the outer edge. You
   can switch-off line numbering by specifying ``nolineno`` in the
   options.

-  ``flushleft``: The University recommends using ragged right or flush
   left alignment for texts. The reason behind this is left justifying a
   text may exclude a certain readers. Dyslexic people find it hard to
   read justified text. You can enable ``raggedright`` option in the
   document class by passing ``flushleft`` argument. Default is flush
   left and right.

Title page
~~~~~~~~~~

The front page (title page) resizes to fit your title length. You can
modify the options in ``thesis-info.tex``.

-  ``\subtitle`` (optional): Adds a subtitle to your thesis.

-  ``\college`` (optional): This option adds the name of your college on
   the bottom left.

If ``\college`` is defined, the bottom of the title page will look like
this:

::

        King's College                                                   2014

If ``\college`` is undefined or blank, the ``degreedate`` will be
centered.

::

                                        2014

The template offers support to having both the college and university
crests or just one of the crests.

-  ``\collegeshield`` (optional): Includes college crest in addition to
   the university crest. This reformats the front page layout.

Abstract separate
~~~~~~~~~~~~~~~~~

-  A separate abstract with the title of the PhD and the candidate name
   has to be submitted to the Student Registry. This can be generated
   using ``abstract`` option in the document class. Ignore subsequent
   warnings about skipping sections (if any).

-  To generate the separate abstract and the title page, make sure the
   following commands are in the preamble section of ``thesis.tex``
   file:

   ::

       \ifdefineAbstract
       \includeonly{Abstract/abstract}
       \fi

Chapter mode
~~~~~~~~~~~~

-  The chapter mode allows user to only print specific chapters along
   with references. By default, it excludes everything else in the front
   matter and appendices. This can done by using ``chapter`` option in
   the document class in ``thesis.tex``. Ignore subsequent warnings
   about skipping sections (if any).

-  To generate the separate abstract and the title page, make sure the
   following commands are in the preamble section of ``thesis.tex``
   file:

   ::

       \ifdefineChapter
           \includeonly{Chapter3/chapter3}
       \fi

Draft
~~~~~

``draft`` adds a watermark ``draft`` text with timestamp and version
number at the top or the bottom of the page. Pagewise line numbering is
added on every page. ``draft`` settings can be tweaked in the
``preamble.tex``.

-  Use ``draftclassic`` in the document class options to use the default
   book class draft mode.

-  To add figures in draft mode (default enabled), in the preamble set
   ``\setkeys{Gin}{draft=false}``. ``draft=true`` disables figures

-  To change the watermark text

-  To change the position of the watermark text. Default watermark
   position is top. The location can be changed to (top / bottom)

-  To change the draft version. Default draft version is v1.0.

-  Watermark grayscale value can be modified. Text grayscale value
   (should be between 0-black and 1-white). Default value is 0.75

Choosing the fonts
~~~~~~~~~~~~~~~~~~

``PhDThesisPSnPDF`` currently supports three fonts ``Times``,
``Fourier`` and ``Latin Modern (default)``.

-  ``times``: (The University of Cambridge guidelines recommend using
   Times). Specifying times option in the document class will use
   ``mathptpx`` or ``Times`` font with Math Support.
-  ``fourier``: fourier font with math support
-  ``default (empty)``: When no font is specified, ``Latin Modern`` is
   used as the default font with Math Support.
-  ``customfont``: Any custom font can be set in preamble by using
   ``customfont`` option in the document class. Then the custom font can
   be loaded in preamble.tex in the line:

   ::

       \ifsetCustomFont
         \RequirePackage{Your_Custom_Font}
       \fi

Choosing the bibliography style
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``PhDThesisPSnPDF`` currently supports two styles ``authoryear`` and
``numbered (default)``. Citation style has to be set. You can also
specify ``custombib`` style and customise the bibliography.

-  ``authoryear``: For author-year citation eg., Krishna (2013)

-  ``numbered``: (Default Option) For numbered and sorted citation e.g.,
   [1,5,2]

-  ``custombib``: Define your own bibliography style in the
   ``preamble.tex`` file.

   ::

       \RequirePackage[square, sort, numbers, authoryear]{natbib}

-  (Overview of Bibtex-Styles with
   preview)[http://nodonn.tipido.net/bibstyle.php?]

-  If you would like to use biblatex instead of natbib. Pass the option
   ``custombib`` in the documentclass. In the ``preamble.tex`` file,
   edit the custombib section. Make sure you don't load the natbib
   package and you can specify the layout of your references in
   ``thesis.tex`` in the reference section. If you are using ``biber``
   as backend, run
   ``pdflatex thesis.tex >> biber thesis >> pdflatex thesis.tex >> biber thesis >> pdflatex thesis.tex``.
   If you are using the default natbib package, don't worry about this.

Choosing the page style
~~~~~~~~~~~~~~~~~~~~~~~

``PhDThesisPSnPDF`` defines 3 different page styles (header and footer).
The following definition is for ``twoside`` layout. To choose a page
style, include it in the ``documentclass`` options:
``\documentclass[PageStyleI]{PhDThesisPSnPDF}``. Alternatively, page
style can be changed by adding ``\pagestyle{PageStyleI}`` or
``\pagestyle{PageStyleII}`` in ``thesis.tex``. Note: Using
``\pagestyle`` command will override ``documentclass`` options when used
globally.

-  ``default (leave empty)``: For Page Numbers in Header (Left Even,
   Right Odd) and Chapter Name in Header (Right Even) and Section #.
   Section Name (Left Odd). Blank Footer.

   ::

       Header (Even)   : 4                                                 Introduction

       Header (Odd)    : 1.2 Section Name                                  5

       Footer          : Empty

-  ``PageStyleI``: For Page Numbers in Header (Left Even, Right Odd) and
   Chapter Name next to the Page Number on Even Side (Left Even).
   Section Number and Section Name and Page Number in Header on Odd Side
   (Right Odd). Footer is empty. Layout:

   ::

       Header (Even)   : 4 | Introduction

       Header (Odd)    :                                                   1.2 Section Name | 5

       Footer          :                               Empty

-  ``PageStyleII``: Chapter Name on Even Side (Left Even) in Header.
   Section Number and Section Name in Header on Odd Side (Right Odd).
   Page numbering in footer. Layout:

   ::

       Header (Even)   : Introduction

       Header (Odd)    :                                                   1.2 Section Name

       Footer[centered]:                               3

Changing the visual style of chapter headings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The visual style of chapter headings can be modified using the
``titlesec`` package. Edit the following lines in the ``preamble.tex``
file.

::

        \RequirePackage{titlesec}
        \newcommand{\PreContentTitleFormat}{\titleformat{\chapter}[display]{\scshape\Large}
        {\Large\filleft{\chaptertitlename} \Huge\thechapter}
        {1ex}{}
        [\vspace{1ex}\titlerule]}
        \newcommand{\ContentTitleFormat}{\titleformat{\chapter}[display]{\scshape\huge}
        {\Large\filleft{\chaptertitlename} \Huge\thechapter}{1ex}
        {\titlerule\vspace{1ex}\filright}
        [\vspace{1ex}\titlerule]}
        \newcommand{\PostContentTitleFormat}{\PreContentTitleFormat}
        \PreContentTitleFormat

Custom settings
~~~~~~~~~~~~~~~

-  The depth for the table of contents can be set using:

   ::

       \setcounter{secnumdepth}{3}
       \setcounter{tocdepth}{3}

   A depth of [3] indicates to a level of ``\subsubsection`` or #.#.#.#.
   Default set as 2.

-  To hide sections from appearing in TOC use:
   ``\tochide\section{Section name}`` in your TeX files

-  Define custom caption style for figure and table caption in
   ``preamble.tex`` using:

   ::

       \RequirePackage[small,bf,figurename=Fig.,labelsep=space,tableposition=top]{caption}

-  Uncomment the following lines in ``preamble.tex`` to force a figure
   to be displayed in a particular location. Use ``H`` when including
   graphics. Note ``H`` instead of ``h``.

   ::

       \usepackage{float}
       \restylefloat{figure}

-  Bibliography with Author-Year Citation in ``preamble.tex``:

   ::

       \RequirePackage[round, sort, numbers, authoryear]{natbib}

-  Line spacing for the entire document can be specified in
   ``preamble.tex``. Uncomment the line spacing you prefer. e.g.,

Nomenclature definition
~~~~~~~~~~~~~~~~~~~~~~~

-  To use nomenclature in your chapters:

   ::

       \nomenclature[g-pi]{$\pi$}{ $\simeq 3.14\ldots$}

   The sort keys have prefix. In this case a prefix of ``g`` is used to
   denote Greek Symbols, followed by ``-pi`` or ``-sort_key``. Use a
   ``-`` to separate sort key from the prefixes. The standard prefixes
   defined in this class are:

   -  ``A`` or ``a``: Roman Symbols

   -  ``G`` or ``g``: Greek Symbols

   -  ``Z`` or ``z``: Acronyms/Abbreviations

   -  ``R`` or ``r``: Superscripts

   -  ``S`` or ``s``: Subscripts

   -  ``X`` or ``x``: Other Symbols

-  You can change the Title of Nomenclature to Notations or Symbols in
   the ``preamble.tex`` using:

   ::

       \renewcommand\nomname{Symbols}

TexStudio's default compile option doesn't include ``nomenclature``, to
compile your document with the nomenclature, do the following:

::

        Options >> Configure TexStudio >> Build >> User Commands >> add user command

In ``add user command`` type ``makenomeclature:makenomenclature`` on the
left pane and ``makeindex %.nlo -s nomencl.ist -o %.nls`` on the
execution side. Now you can run the user defined command
``makenomenclature`` from ``Tools >> User >> makenomenclature``.

Alternatively, you can use the ``compile-thesis-windows.bat`` file or
run ``make`` on Unix / Linux / MacOS

Git hooks
++++++++++++

You rarely want to commit changes to your TeX files which are not
reflected in the PDF included in the repo. You can automate this
process, among other things, with a git hook. Install the hook with
``make hooks`` (or see how to do it in ``./hooks/install.sh``). Now
every time you commit, if any files affecting your build have changed in
this commit and those changes are more recent than the last modification
of ``thesis.pdf``, the default ``make`` target will be run and changes
to ``thesis.pdf`` will be ``git add``\ ed.

Currently, changes to any tex/pdf/eps/png/cls files are picked up. This
can be changed in ``./hooks/pre-commit``.

Skip the hook with ``git commit --no-verify``.

``bash``-only.

General guidelines
++++++++++++++++++++++

-  To restrict the length of the figure caption in List of figures use a
   [short-title] and {longtitle} for the caption or the section:

   ::

       `\caption[Caption that you want to appear in TOC]{Actual caption of the figure}`
       `\section[short]{title}`

-  To exclude sections from being numbered and disable it from appearing
   in the Table of Contents use or

-  To only exclude it from being listed in the Table of Contents
   encapsulate the section command inside the ``\tochide`` command.
   ``\tochide{\section{Section_Name}}`` the section will not appear in
   the Table of Contents, but the section will be numbered.

-  When including figures in your tex file, it's a good practice to size
   your picture depending on the page size, instead of using absolute
   values. In the following example ``0.75\textwidth`` refers to picture
   width being set to 75% of the text width.

   ::

       \includegraphics[width=0.75\textwidth]{minion}

-  Use a ``-`` to separate sort key from the prefixes, eg., ``g-pi``
   denotes the Greek symbol ``pi``.
