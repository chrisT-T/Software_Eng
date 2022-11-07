from flask import Blueprint, flash, jsonify, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from app.model.login import User
from app.service.user import UserService

bp = Blueprint('auth', __name__)

service = UserService()

@bp.route('/auth/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    username = form['username']
    password = form['password']
    if username:
        user = service.find_user(username)
        if user:
            if user.validate_password(password):
                login_user(user)
                return jsonify({"msg": "Login Success"}), 200
        else:
            return jsonify({"msg": "Username Or Password Error"}), 404
    else:
        return jsonify({"msg": "Invalid username"}), 400


@bp.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/index.html'))
