from app.extensions import db

class Project(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    creater_name = db.Column(db.String(32))
    project_name = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)
    project_language = db.Column(db.Enum('python', 'cpp', 'typescript'))

