from flask import Blueprint, request
from flask_login import login_required, login_user, logout_user

from app.service.user import UserService

bp = Blueprint('login', __name__)

service = UserService()


@bp.route('/api/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    username = form['username']
    password = form['password']
    if username:
        user, flag = service.find_user_by_username(username)
        if flag:
            if user.validate_password(password):
                login_user(user)
                return "", 204
        else:
            return "Username or password error", 404
    else:
        return "Invalid username", 400


@bp.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return "", 204
