from flask import Blueprint

bp = Blueprint('auth', __name__)

from {{cookiecutter.project_slug}}.auth import routes  # noqa: E402, F401
