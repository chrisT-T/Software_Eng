from app.model import login
from app.extensions import db
from werkzeug.security import generate_password_hash


class UserService():
    def create_user(self, username, password):
        print("testhere")
        max_id_user = login.User.query.order_by('id').first()
        print(max_id_user.id)
        new_user = login.User(id=max_id_user.id + 1, username=username,
                              password_hash=generate_password_hash(password))
        print(new_user.id)
        db.session.add(new_user)
        db.session.commit()

        print("finish create user")
