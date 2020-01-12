from flask import render_template, redirect, url_for, session, request
from ..app import app


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/language/<language>')
def set_language(language=None):
    """
    This route is requested, whenever (and only if) the user changed the language manually
    """

    session['language'] = language
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
