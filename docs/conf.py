#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ---------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

templates_path = ["_templates"]

source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"cookietemple"
copyright = u"2020, Lukas Heumos, Philipp Ehmele, the cookiejar organization"
author = u"Lukas Heumos, Philipp Ehmele, the cookiejar organization"

version = "1.3.4"
release = "1.3.4"

language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output -------------------------------------------

html_theme = "sphinx_rtd_theme"

# html_theme_options = {}

html_static_path = ["_static"]


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "cookietempledoc"


# -- Options for LaTeX output ------------------------------------------

latex_elements: Dict[str, str] = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (master_doc, "cookietemple.tex", "cookietemple Documentation", "Lukas Heumos, Philipp Ehmele", "manual"),
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "cookietemple", "cookietemple Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "cookietemple",
        "cookietemple Documentation",
        author,
        "cookietemple",
        "One line description of project.",
        "Miscellaneous",
    ),
]

html_css_files = [
    "custom_cookietemple.css",
]
