import logging
import sys

from coalib.coala import main as run_coala

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger('cookietemple lint')
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def lint_project():
    """
    TODO
    """
    sys.exit(run_coala())
