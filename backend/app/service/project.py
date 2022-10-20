import datetime
import time
from app.extensions import db
from app.model.project import Project


class ProjectService():
    def create_project(self,
                       creator_id,
                       project_name,
                       project_language):
        try:

            select_res = Project.query.order_by(Project.id.desc())
            if len(select_res.all()) == 0:
                max_id = 0
            else:
                max_id = select_res.first().id
            new_project = Project(id=max_id + 1,
                                  creator_id=creator_id,
                                  create_time=datetime.date.fromtimestamp(time.time()),
                                  project_name=project_name,
                                  project_language=project_language)
            db.session.add(new_project)
            db.session.commit()
            return 'ok'
        except Exception as e: # noqa
            print(e)
            return 'create project failed'
