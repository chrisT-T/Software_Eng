from flask import Blueprint, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from app.model.login import User
from app.service.user import UserService

bp = Blueprint('auth', __name__)
service = UserService()

service = UserService()


@bp.route('/auth/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    username = form['username']
    password = form['password']
    if username:
        user, flag = service.find_user_by_username(username)
        if flag:
            if user.validate_password(password):
                login_user(user)
                return {"msg": "Login Success"}, 200
        else:
            return {"msg": "Username or password error"}, 404
    else:
        return {"msg": "Invalid username"}, 400


@bp.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return "user logout"
