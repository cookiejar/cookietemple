.. _adding_templates:

============================
Adding new templates
============================

Adding new templates is one of the major improvements and community contributions to COOKIETEMPLE, which is why we are dedicating a whole section to it.
Due to the tight coupling of our templates with all COOKIETEMPLE commands such as :code:`create`, :code:`list`, :code:`info`, :code:`lint` and :code:`bump-version`,
new templates require the modification of several files.

The following sections will line out the requirements for new templates and guide you through the process of adding new templates step by step.
Nevertheless, we strongly encourage you to discuss your proposed template first with us in public *via* a Github issue.

Template requirements
-----------------------
To keep the standard of our templates high we enforce several standards, to which all templates **must** adhere.
Exceptions, where applicable, but they would have to be discussed beforehand. Hence, the term *should*.

1. | New templates should be novel.
   | We do not want a second cli-python template, but you are of course always invited to improve it. A new commandline library does not warrant an additional template, but rather modifications of the existing template with cookiecutter if statements.
   | However, distinct modifications of already existing templates may be eligible. An example would be to add a GUI template for a language, which does not yet have a GUI template.
   | Templates for domains, which we do not yet cover or additional languages to already existing domains are of course more than welcome.

2. | All templates should be cutting edge and not be based on technical debt or obscure requirements. Our target audience are enthusiastic open source contributors and not decade old companies stuck with Python 2.7.

3. All templates should build as automatically as possible and download all dependencies without manual intervention.

4. All templates should have a testing and possibly mocking framework included.

5. All templates should provide a readthedocs setup (include changelog and a codeofconduct), a README.rst file, a LICENSE, Github issue and pull request templates and a .gitignore file. Note that most of these are already included in our common_files and do not need to be rewritten. More on that below.

6. All templates should privde a Makefile, which wraps heavily used commands to unify common operations such as installing, testing or distributing a project, independent of the language

7. All templates should have a Dockerfile, which provides an entrypoint for the project.

8. All templates must implement all required functionality to allow the application of all commands mentioned above to them.

9. All templates should have Github workflows, which at least build the documentation and the project.

10. Every template should also have a workflow inside COOKIETEMPLE, which creates a project from the template with dummy values

11. Your template should support Linux and MacOS. Windows support is optional, but strongly encouraged.

Again, we strongly suggest that new templates are discussed with the core team first.

Step by step guide to adding new templates
------------------------------------------

Let's assume that we are planning to add a new commandline `Brainfuck <https://en.wikipedia.org/wiki/Brainfuck>`_ template to COOKIETEMPLE.
We discussed our design at length with the core team and they approved our plan. For the sake of this tutorial we assume that the path / always points to /cookietemple.
Hence, at this level we see :code:`cookietemple_cli.py` and a folder per CLI command.

1. | Add our brainfuck template information to :code:`/create/templates/available_templates.yml`.

.. figure:: images/adding_templates_step_1.png
   :scale: 100 %
   :alt: Available Templates Brainfuck example

   Addition of a cli-brainfuck template to available_templates.yml.

2. 
