from flask import render_template
from {{cookiecutter.project_slug_no_hyphen}}.errors import bp

{% if cookiecutter.setup_type == 'advanced' -%}
from {{ cookiecutter.project_slug_no_hyphen }}.config import db{% endif %}


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    {% if cookiecutter.setup_type == 'advanced' -%}
    db.session.rollback(){% endif %}
    return render_template('errors/500.html'), 500
