from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager
from app.model.relation_tables import (admin_table, editable_table,
                                       pending_table, readonly_table)


class User(db.Model, UserMixin):
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    created_projects = db.relationship("Project", back_populates="creator")
    readonly_projects = db.relationship("Project", secondary=readonly_table, back_populates="readonly_users")
    editable_projects = db.relationship("Project", secondary=editable_table, back_populates="editable_users")
    admin_projects = db.relationship("Project", secondary=admin_table, back_populates="admin_users")
    pending_projects = db.relationship("Project", secondary=pending_table, back_populates="pending_users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
