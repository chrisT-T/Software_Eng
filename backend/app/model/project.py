from app.extensions import db


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)
    project_language = db.Column(db.Enum('python', 'cpp', 'typescript'))
    docker_id = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    creator = db.relationship("User", back_populates="created_projects")
