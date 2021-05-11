import os

{% if cookiecutter.setup_type == 'advanced' -%}
import configparser

from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()
{% endif %}
class Config:
    CURRENT_DIR = os.path.abspath(os.getcwd())
    MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(MODULE_DIR, 'static')
    TEMPLATES_PATH = os.path.join(MODULE_DIR, 'templates')
    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOME_SUPERSECRETKEY'
    {% if cookiecutter.setup_type == 'advanced' -%}
    LANGUAGES = {
        'en': 'English',
        'de': 'German'
    }

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.abspath(os.getcwd())+"/{{ cookiecutter.project_slug_no_hyphen }}/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'


def config_mail(app):
    try:
        config = configparser.ConfigParser()
        config.read(Config.STATIC_PATH + '/mail.conf')
        mail_username = config['DEFAULT']['gmail_user_name']
        mail_password = config['DEFAULT']['gmail_password']

        # EMAIL SETTINGS
        app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME=mail_username,
            MAIL_PASSWORD=mail_password
        )
    except KeyError:
        # EMAIL SETTINGS
        app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME="username_not_available",
            MAIL_PASSWORD="password_not_available"
        )
        {% endif %}
