#!/usr/bin/env python

"""Tests for `{{cookiecutter.project_slug}}` package."""
import pytest
from flask import Flask
from {{cookiecutter.project_slug_no_hyphen}}.config import Config

{% if cookiecutter.setup_type == 'advanced' -%}
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

{% endif %}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

{% if cookiecutter.setup_type == 'advanced' -%}
def create_test_app():
    migrate = Migrate()
    db = SQLAlchemy()
    login = LoginManager()
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'
    bootstrap = Bootstrap()
    babel = Babel()

    app = Flask(__name__)
    app.config.from_object(Config)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)

    from {{cookiecutter.project_slug}}.errors import bp as errors_bp  # noqa: E402

    app.register_blueprint(errors_bp)

    from {{cookiecutter.project_slug}}.auth import bp as auth_bp  # noqa: E402

    app.register_blueprint(auth_bp, url_prefix='/auth')

    from {{cookiecutter.project_slug}}.main import bp as main_bp  # noqa: E402

    app.register_blueprint(main_bp)

    return app


def test_redirect():
    flask_app = create_test_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    response = testing_client.get('/')
    assert response.status_code == 302  # assert redirecting
    {% endif %}
{% if cookiecutter.setup_type == 'basic' -%}


def create_test_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from {{cookiecutter.project_slug_no_hyphen}}.errors import bp as errors_bp  # noqa: E402

    app.register_blueprint(errors_bp)

    from {{cookiecutter.project_slug_no_hyphen}}.basic import bp as basic_bp

    app.register_blueprint(basic_bp)

    return app


def test_redirect():
    flask_app = create_test_app()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
    response = testing_client.get('/')
    assert response.status_code == 302  # assert redirecting
    {% endif %}
