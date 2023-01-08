import datetime

from app.extensions import db
from app.model.relation_tables import (admin_table, editable_table,
                                       pending_table, readonly_table)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(32))
    hash_id = db.Column(db.String(32))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())
    project_language = db.Column(db.String(32))
    docker_id = db.Column(db.Text)
    path = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    creator = db.relationship("User", back_populates="created_projects")

    # n * m relationship by second table
    readonly_users = db.relationship("User", secondary=readonly_table, back_populates="readonly_projects")
    editable_users = db.relationship("User", secondary=editable_table, back_populates="editable_projects")
    admin_users = db.relationship("User", secondary=admin_table, back_populates="admin_projects")
    pending_users = db.relationship("User", secondary=pending_table, back_populates="pending_projects")
