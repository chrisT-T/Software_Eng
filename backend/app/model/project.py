from app.extensions import db


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.String(128), primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    project_name = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)
    project_language = db.Column(db.Enum('python', 'cpp', 'typescript'))
