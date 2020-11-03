.. _adding_templates:

============================
Adding new templates
============================

Adding new templates is one of the major improvements and community contributions to cookietemple, which is why we are dedicating a whole section to it.
Please note that creating new templates is a time consuming task. So be prepared to invest a few hours to bring a new template to life.
The integration into cookietemple however, is straightforward if you follow the guide below.
Due to the tight coupling of our templates with all cookietemple commands such as :code:`create`, :code:`list`, :code:`info`, :code:`lint` and :code:`bump-version`,
new templates require the modification of several files.

cookietemple uses `cookiecutter <https://cookiecutter.readthedocs.io/en/1.7.2/>`_ to create all templates.
You need to familiarize yourself beforehand with cookiecutter to able to write templates, but don't worry, it's pretty easy and you usually get by with very few cookiecutter variables.
You can start with your `very first cookiecutter template <https://cookiecutter.readthedocs.io/en/1.7.2/first_steps.html>`_ and then simply see how the other existing cookietemple templates are made and copy what you need.

The following sections will line out the requirements for new templates and guide you through the process of adding new templates step by step.
Nevertheless, we strongly encourage you to discuss your proposed template first with us in public *via* a Github issue.

Template requirements
-----------------------
To keep the standard of our templates high we enforce several standards, to which all templates **must** adhere.
Exceptions, where applicable, but they would have to be discussed beforehand. Hence, the term *should*.

1. New templates must be novel.
   We do not want a second cli-python template, but you are of course always invited to improve it. A new commandline library does not warrant an additional template, but rather modifications of the existing template with cookiecutter if statements.
   However, distinct modifications of already existing templates may be eligible. An example would be to add a GUI template for a language, which does not yet have a GUI template.
   Templates for domains, which we do not yet cover or additional languages to already existing domains are of course more than welcome.

2. All templates should be cutting edge and not be based on technical debt or obscure requirements. Our target audience are enthusiastic open source contributors and not decades old companies stuck with Python 2.7.

3. All templates should build as automatically as possible and download all dependencies without manual intervention.

4. All templates must have a testing and possibly mocking framework included.

5. All templates must provide a readthedocs setup, a README.rst, usage.rst and installation.rst file, a LICENSE, Github issue and pull request templates and a .gitignore file. Moreover, a .dependabot configuration should be present if applicable.
   Note that most of these are already included in our common_files and do not need to be rewritten. More on that below.

6. All templates must provide a Makefile, which wraps heavily used commands to unify common operations such as installing, testing or distributing a project.

7. All templates should have a Dockerfile, which provides an entrypoint for the project.

8. All templates must implement all required functionality to allow the application of all commands mentioned above to them, which includes a cookietemple.cfg file, the template being in the available_templates.yml and more.

9. All templates must have Github workflows, which at least build the documentation and the project.

10. Every template must also have a workflow inside cookietemple, which creates a project from the template with dummy values.

11. Your template must support Linux and MacOS. Windows support is optional, but strongly encouraged.

Again, we strongly suggest that new templates are discussed with the core team first.

Step by step guide to adding new templates
------------------------------------------

Let's assume that we are planning to add a new commandline `Brainfuck <https://en.wikipedia.org/wiki/Brainfuck>`_ template to cookietemple.
We discussed our design at length with the core team and they approved our plan. For the sake of this tutorial **we assume that the path / always points to /cookietemple**.
Hence, at this level we see ``cookietemple_cli.py`` and a folder per CLI command.

1. Let's add our brainfuck template information to ``/create/templates/available_templates.yml`` below the ``cli`` section.

.. code-block::
    :linenos:

    cli:
        brainfuck:
            name: Brainfuck Commandline Tool
            handle: cli-brainfuck
            version: 0.0.1
            available libraries: none
            short description: Brainfuck Commandline tool with ANSI coloring
            long description: Amazing brainfuck tool, which can even show pretty unicorns in the console.
                Due to ANSI coloring support they can even be pink! Please someone send help.

2. | Next, we add our brainfuck template to :code:`/create/templates`
   | Note that it should adhere to the standards mentioned above and include all required files. Don't forget to add a cookietemple.cfg file to facilitate bump-version. See :ref:`bump-version-configuration` for details.
    It is **mandatory** to name the top level folder ``{{ cookiecutter.project_slug }}``, which ensures that the project after creation will have a proper name.
    Furthermore, the ``cookiecutter.json`` file should have at least the following variables:

.. code-block::
    :linenos:

    {
    "full_name": "Homer Simpson",
    "email": "homer.simpson@posteo.net",
    "project_name": "sample-cli",
    "project_slug": "sample-cli",
    "version": "1.0.0",
    "project_short_description": "Command-line utility to...",
    "github_username": "homer_github"
    }

The file tree of the template should resemble

.. code-block::
    :linenos:

    ├── cookiecutter.json
    └── {{ cookiecutter.project_slug }}
        ├── docs
        │   ├── installation.rst
        │   └── usage.rst
        ├── .github
        │   └── workflows
        │       └── build_brainfuck.yml
        ├── hello.bf
        ├── cookietemple.cfg
        └── README.rst

3. | Now it is time to subclass the :code:`TemplateCreator` to implement all required functions to create our template!
   | Let's edit ``/create/domains/cli_creator.py``. Note that for new domains you would simply create a new file called DomainCreator.
   | In this case we suggest to simply copy the code of an existing Creator and adapt it to the new domain. Your new domain may make use of other creation functions instead of :code:`create_template_without_subdomain`, if they for example contain subdomains. You can examine :code:`create/TemplatorCreator.py` to see what's available. You may also remove functions such as the creation of common files.
   | If we have any brainfuck specific cookiecutter variables that we need to populate, we may add them to the TemplateStructCli.
   | Our brainfuck templates does not have them, so we just leave it as is.
   | For the next step we simply go through the :code:`CliCreator` class and add our brainfuck template where required. Moreover, we implement a :code:`cli_brainfuck_options` function, which we use to prompt for template specific cookiecutter variables.
   | Assuming ``cli_creator.py`` already contains a ``cli-java`` template

.. code-block:: python
    :linenos:

    @dataclass
    class TemplateStructCli(CookietempleTemplateStruct):
        """
        Intended Use: This class holds all attributes specific for CLI projects
        """

        """______JAVA______"""
        main_class_prefix: str = ''

        """____BRAINFUCK___"""


    class CliCreator(TemplateCreator):

        def __init__(self):
            self.cli_struct = TemplateStructCli(domain='cli')
            super().__init__(self.cli_struct)
            self.WD = os.path.dirname(__file__)
            self.WD_Path = Path(self.WD)
            self.TEMPLATES_CLI_PATH = f'{self.WD_Path.parent}/templates/cli'

            '"" TEMPLATE VERSIONS ""'
            self.CLI_JAVA_TEMPLATE_VERSION = super().load_version('cli-java')
            self.CLI_BRAINFUCK_TEMPLATE_VERSION = super().load_version('cli-brainfuck')

        def create_template(self, dot_cookietemple: dict or None):
            """
            Handles the CLI domain. Prompts the user for the language, general and domain specific options.
            """

            self.cli_struct.language = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                    question='Choose the project\'s primary language',
                                                                                    choices=['python', 'java', 'brainfuck'],
                                                                                    default='python',
                                                                                    dot_cookietemple=dot_cookietemple,
                                                                                    to_get_property='language')

            # prompt the user to fetch general template configurations
            super().prompt_general_template_configuration(dot_cookietemple)

            # switch case statement to prompt the user to fetch template specific configurations
            switcher = {
                'java': self.cli_java_options,
                'brainfuck': self.cli_brainfuck_options
            }
            switcher.get(self.cli_struct.language)(dot_cookietemple)

            self.cli_struct.is_github_repo, \
                self.cli_struct.is_repo_private, \
                self.cli_struct.is_github_orga, \
                self.cli_struct.github_orga \
                = prompt_github_repo(dot_cookietemple)

            if self.cli_struct.is_github_orga:
                self.cli_struct.github_username = self.cli_struct.github_orga

            # create the chosen and configured template
            super().create_template_without_subdomain(f'{self.TEMPLATES_CLI_PATH}')

            # switch case statement to fetch the template version
            switcher_version = {
                'java': self.CLI_JAVA_TEMPLATE_VERSION,
                'brainfuck': self.CLI_BRAINFUCK_TEMPLATE_VERSION
            }
            self.cli_struct.template_version, self.cli_struct.template_handle = switcher_version.get(
                self.cli_struct.language.lower()), f'cli-{self.cli_struct.language.lower()}'

            super().process_common_operations(domain='cli', language=self.cli_struct.language, dot_cookietemple=dot_cookietemple)

        def cli_python_options(self, dot_cookietemple: dict or None):
            """ Prompts for cli-python specific options and saves them into the CookietempleTemplateStruct """
            self.cli_struct.command_line_interface = cookietemple_questionary_or_dot_cookietemple(function='select',
                                                                                                question='Choose a command line library',
                                                                                                choices=['Click', 'Argparse', 'No command-line interface'],
                                                                                                default='Click',
                                                                                                dot_cookietemple=dot_cookietemple,
                                                                                                to_get_property='command_line_interface')
            [...]

        def cli_java_options(self, dot_cookietemple: dict or None) -> None:
            """ Prompts for cli-java specific options and saves them into the CookietempleTemplateStruct """
            [...]

        def cli_brainfuck_options(self):
            """ Prompts for cli-brainfuck specific options and saves them into the CookietempleTemplateStruct """
            pass


4. | If a new template were added we would also have to import our new Creator in :code:`create/create.py` and add the new domain to the domain prompt and the switcher.
   | However, in this case we can simply skip this step, since ``cli`` is already included.

.. code-block::
    :linenos:

    def choose_domain(domain: str):
        """
        Prompts the user for the template domain.
        Creates the .cookietemple file.
        Prompts the user whether or not to create a Github repository
        :param domain: Template domain
        """
        if not domain:
            domain = click.prompt('Choose between the following domains',
                                type=click.Choice(['cli', 'gui', 'web', 'pub']))

        switcher = {
            'cli': CliCreator,
            'web': WebCreator,
            'gui': GuiCreator,
            'pub': PubCreator
        }

        creator_obj = switcher.get(domain.lower())()
        creator_obj.create_template()

5. | Linting is up next! We need to ensure that our brainfuck template always adheres to the highest standards! Let's edit :code:`lint/domains/cli.py`.
   | We need to add a new class, which inherits from TemplateLinter and add our linting functions to it.

.. code-block:: python
    :linenos:

    class CliBrainfuckLint(TemplateLinter, metaclass=GetLintingFunctionsMeta):
        def __init__(self, path):
            super().__init__(path)

        def lint(self):
            super().lint_project(self, self.methods)

        def brainfuck_files_exist(self) -> None:
            """
            Checks a given pipeline directory for required files.
            Iterates through the templates's directory content and checkmarks files for presence.
            Files that **must** be present::
                'hello.bf',
            Files that *should* be present::
                '.github/workflows/build_brainfuck.yml',
            Files that *must not* be present::
                none
            Files that *should not* be present::
                none
            """

            # NB: Should all be files, not directories
            # List of lists. Passes if any of the files in the sublist are found.
            files_fail = [
                ['hello.bf'],
            ]
            files_warn = [
                [os.path.join('.github', 'workflows', 'build_brainfuck.yml')],
            ]

            # List of strings. Fails / warns if any of the strings exist.
            files_fail_ifexists = [

            ]
            files_warn_ifexists = [

            ]

            files_exist_linting(self, files_fail, files_fail_ifexists, files_warn, files_warn_ifexists)


We need to ensure that our new linting function is found when linting is applied. Therefore, we turn our eyes to :code:`lint/lint.py`, import our CliBrainfuckLinter and add it to the switcher.

.. code-block:: python
    :linenos:

    from cookietemple.lint.domains.cli import CliBrainfuckLint

    switcher = {
        'cli-python': CliPythonLint,
        'cli-java': CliJavaLint,
        'cli-brainfuck': CliBrainfuckLint,
        'web-website-python': WebWebsitePythonLint,
        'gui-java': GuiJavaLint,
        'pub-thesis-latex': PubLatexLint
    }

Our shiny new CliBrainfuckLinter is now ready for action!

6. | Now it´s time to add some tests for our new template

   It´s important to add tests for the new template to cookietemple, at least you should
   test the creation and linting of the new template, besides any special code that comes with the new template.
   The tests are located inside the :code:`tests` directory. If you developed a new template
   make sure to add the new :code:`Linter` and/or :code:`Creator`. Please note, that you have to name your test files and functions like
   :code:`test_*` otherwise they won´t be recognized by :code:`pytest`. Examine the tests for the other templates to adapt them to your template.

   You can run the tests using the :code:`tox` command. Make sure you run this command inside the directory where the :code:`tox.ini` file is.
   An important note when using :code:`tox`: Tox is designed to run inside :code:`virtualenv` and not with :code:`conda`. Depending on your OS,
   your python version or your environment you may run into an :code:`InterpreterNotFound-Exception`. To fix this, you may have to change :code:`envlist = py37, py38, flake8`
   to :code:`envlist = python3.7, python3.8, flake8`.

   Another more simple option is to run :code:`make test` to run all tests (make sure your in the top level directory of cookietemple when calling this command).


7. | The only thing left to do now is to add a new Github Actions workflow for our template. Let's go one level up in the folder tree and create :code:`.github/workflows/create_cli_brainfuck.yml`.
   | We want to ensure that if we change something in our template, that it still builds!

.. code-block:: bash
    :linenos:

    name: Create cli-brainfuck Template

    on: [push]

    jobs:
      build:

          runs-on: ubuntu-latest
          strategy:
            matrix:
              python: [3.7, 3.8]

          steps:
          - uses: actions/checkout@v2
            name: Check out source-code repository

          - name: Setup Python
            uses: actions/setup-python@v1
            with:
              python-version: ${{ matrix.python }}

          - name: Build cookietemple
            run: |
              python setup.py clean --all install

          - name: Create cli-brainfuck Template
            run: |
              echo -e "cli\nbrainfuck\nHomer\nhomer.simpson@hotmail.com\nExplodingSpringfield\ndescription\nhomergithub\nn" | cookietemple create

          - name: Build Package
            uses: fabasoad/setup-brainfuck-action@master
            with:
              version: 0.1.dev1
          - name: Hello World
            run: |
              brainfucky --file ExplodingSpringfield/hello.bf


    We were pleasently surprised to see that someone already made a Github Action for brainfuck.

8. | Finally, we add some documentation to :code:`/docs/available_templates.rst` and explain the purpose, design and frameworks/libraries.

   That's it! We should now be able to try out your new template using :code:`cookietemple create`
   The template should be creatable, it should automatically lint after the creation and Github support should be enabled as well! If we run :code:`cookietemple list`
   Our new template should show up as well!
   I'm sure that you noticed that there's not actually a brainfuck template in cookietemple (yet!).

   To quote our mighty Math professors: 'We'll leave this as an exercise to the reader.'
