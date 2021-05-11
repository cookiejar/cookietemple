from flask import redirect, render_template, url_for
from {{cookiecutter.project_slug_no_hyphen}}.basic import bp


@bp.route('/')
def root():
    return redirect((url_for('basic.index')))

{%- if cookiecutter.frontend == 'none' %}
@bp.route('/index')
def index():
    return render_template('basic_index.html'){%- endif %}


{%- if cookiecutter.frontend == '' %}
@bp.route('/index')
def index():
    return render_template('basic_index.html'){%- endif %}

{%- if cookiecutter.frontend.lower() == 'solidstate' %}
@bp.route('/index')
def index():
    return render_template('basic_index_f.html'){%- endif %}
