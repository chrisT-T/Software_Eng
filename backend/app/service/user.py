from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model.user import User


class UserService():
    def create_user(self, username, password, email):
        user = User.query.filter_by(username=username).first()
        if user:
            return "user exists", False
        user = User.query.filter_by(email=email).first()
        if user:
            return "user exists", False
        new_user = User(username=username,
                              password_hash=generate_password_hash(password),
                              email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id, True

    def find_user_by_username(self, username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                return user, True
            return 'no such user', False
        except Exception as e:
            print(e)
            return 'Exception in finding user', False

    def find_user_by_id(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                return user, True
            return 'no such user', False
        except Exception as e:
            print(e)
            return 'Exception in finding user', False

    def find_user_by_email(self, email):
        try:
            user = User.query.filter_by(id=email).first()
            if user:
                return user, True
            return 'no such user', False
        except Exception as e:
            print(e)
            return 'Exception in finding user', False
