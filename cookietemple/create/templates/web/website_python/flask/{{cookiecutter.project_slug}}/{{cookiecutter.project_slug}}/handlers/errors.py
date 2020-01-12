from flask import render_template
from ..app import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(410)
def page_gone(error):
    return render_template('errors/410.html'), 410


@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400
