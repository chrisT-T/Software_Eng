from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model import login


class UserService():
    def create_user(self, username, password):
        user = login.User.query.filter_by(username=username).first()
        if user:
            return {"flag": False, "result": "user exists"}
        max_id_user = login.User.query.order_by(login.User.id.desc()).first()
        print(max_id_user.id)
        new_user = login.User(id=max_id_user.id + 1, username=username,
                              password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return {"flag": True, "result": max_id_user.id}

    def find_user_by_username(self, username):
        try:
            user = login.User.query.filter_by(username=username).first()
            if user:
                return {"flag": True, "result": user}
            return {"flag": False, "result": 'no such user'}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in finding user'}
    def find_user_by_id(self, id):
        try:
            user = login.User.query.filter_by(id=id).first()
            if user:
                return {"flag": True, "result": user}
            return {"flag": False, "result": 'no such user'}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in finding user'}