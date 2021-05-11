from flask import Blueprint

bp = Blueprint('errors', __name__)

from {{cookiecutter.project_slug_no_hyphen}}.errors import handlers  # noqa: E402, F401
