import time
from app.extensions import db
from app.model.project import Project


class projectService():
    def create_project(self,
                       creator_id,
                       project_name,
                       create_time,
                       project_language):
        max_id_project = Project.query.order_by(
            Project.creator_id.desc()).first()
        new_project = Project(id=max_id_project.id + 1,
                              create_time=time.time(),
                              project_name=project_name,
                              project_language=project_language)
        db.session.add(new_project)
        db.session.commit()
