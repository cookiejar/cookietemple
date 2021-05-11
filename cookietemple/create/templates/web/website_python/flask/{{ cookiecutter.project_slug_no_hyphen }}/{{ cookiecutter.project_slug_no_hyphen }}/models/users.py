from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from {{cookiecutter.project_slug_no_hyphen}}.config import db, login


class User(UserMixin, db.Model):
    """
    Just a simple user model with an id as primary key, username, email and the password hash
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
