from app.extensions import db

readonly_table = db.Table(
    "readonly_table",
    db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True)
)

editable_table = db.Table(
    "editable_table",
    db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True)
)

admin_table = db.Table(
    "admin_table",
    db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True)
)

pending_table = db.Table(
    "pending_table",
    db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True)
)
