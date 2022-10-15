from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from requests import request
from app.model.login import User
from .forms import LoginForm
from flask import Blueprint

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                login_user()
                flash('You are logged in now.')
                return redirect(request.args.get('next') 
                                or url_for('/index.html'))
        else:
            flash('Failed to log in. Wrong username or password.')
    if form.errors:
        flash('Failed to log in.')
    return render_template('login.html', form=form)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You are no longer logged in.')
    return redirect(url_for('/index.html'))
