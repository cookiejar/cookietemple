import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CURRENT_DIR = os.path.abspath(os.getcwd())
    MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(MODULE_DIR, 'static')
    TEMPLATES_PATH = os.path.join(MODULE_DIR, 'templates')

    LANGUAGES = {
        'en': 'English',
        'de': 'German'
    }

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SOME_SUPERSECRETKEY'
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
