from flask import flash, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from {{cookiecutter.project_slug_no_hyphen}}.auth import bp
from {{cookiecutter.project_slug_no_hyphen}}.auth.forms.login_form import LoginForm
from {{cookiecutter.project_slug_no_hyphen}}.auth.forms.register_form import RegistrationForm
from {{cookiecutter.project_slug_no_hyphen}}.config import db
from {{cookiecutter.project_slug_no_hyphen}}.models.users import User


@bp.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'),
                           form=form)
