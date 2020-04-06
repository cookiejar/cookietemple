import os

from cookietemple.linting.TemplateLinter import TemplateLinter, files_exist_linting

CWD = os.getcwd()


class PubLatexLint(TemplateLinter):
    def __init__(self, path):
        super().__init__(path)

    def lint(self, label):
        methods = []
        super().lint_project(self, methods, label=label)
