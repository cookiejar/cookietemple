from flask import redirect, render_template, session, url_for
from {{cookiecutter.project_slug_no_hyphen}}.main import bp


@bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('main.index'))


@bp.route('/')
def root():
    return redirect(url_for('main.index'))


@bp.route('/index')
def index():
    return render_template('index.html')
