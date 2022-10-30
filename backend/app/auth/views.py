from flask import Blueprint, flash, jsonify, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from app.model.login import User
from app.service.user import UserService

bp = Blueprint('auth', __name__)


@bp.route('/auth/login', methods=['POST'])
def login():
    form = request.form.to_dict()
    username = form['username']
    password = form['password']
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            if(user.validate_password(password)):
                login_user(user)
                return jsonify({"code": 200, "msg": "Login Success"})
        else:
            return jsonify({"code": 400, "msg": "Username Or Password Error"})


@bp.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/index.html'))
