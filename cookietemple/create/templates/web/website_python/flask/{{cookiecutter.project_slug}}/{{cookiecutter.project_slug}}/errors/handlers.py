from {{cookiecutter.project_slug}}.errors import bp
from flask import render_template
{ % if cookiecutter.is_basic_website == 'n' - %}
from {{cookiecutter.project_slug}}.config import db{ % endif % }


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    { % if cookiecutter.is_basic_website == 'n' - %}
    db.session.rollback(){ % endif % }
    return render_template('errors/500.html'), 500
