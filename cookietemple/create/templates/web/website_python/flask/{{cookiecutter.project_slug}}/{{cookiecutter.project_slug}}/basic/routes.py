from flask import render_template, redirect, url_for

from {{cookiecutter.project_slug}}.basic import bp


@bp.route('/')
def root():
    return redirect((url_for('basic.index')))


@bp.route('/index')
def index():
    return render_template('basic/basic.html')
