from flask import Blueprint

bp = Blueprint('main', __name__)

from {{cookiecutter.project_slug}}.main import routes  # noqa: E402, F401
