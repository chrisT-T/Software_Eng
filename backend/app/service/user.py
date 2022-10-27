from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model import login


class UserService():
    def create_user(self, username, password):
        print("start create")
        max_id_user = login.User.query.order_by(login.User.id.desc()).first()
        print(max_id_user.id)
        new_user = login.User(id=max_id_user.id + 1, username=username,
                              password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
