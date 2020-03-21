import os

from cookietemple.linting.PipelineLint import PipelineLint
from cookietemple.util.dir_util import pf


class CliPythonLint(PipelineLint):
    def __init__(self):
        super().__init__()

    def lint_python(self):
        methods = ['python_files_exist']
        super().lint_pipeline(self, methods)

    def python_files_exist(self):

        files_fail = [
            ['Dockerfile'],
        ]

        # Files that cause an error if they don't exist
        for files in files_fail:
            if any([os.path.isfile(pf(self, f)) for f in files]):
                self.passed.append((1, f'File found: {super()._bold_list_items(files)}'))
                self.files.extend(files)
            else:
                self.failed.append((1, f'File not found: {super()._bold_list_items(files)}'))
