import datetime
import os
import time

import docker
from flask import current_app
from werkzeug.security import generate_password_hash

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

            # create project root_dir
            project_root_dir = (f'{max_id+1}-{project_name}-{project_language}')
            rootdir = current_app.config['ROOT_DIR']
            project_root_path = f'{rootdir}/{project_root_dir}'
            project_root_path = os.path.abspath(project_root_path)
            try:
                os.makedirs(project_root_path)
            except:  # noqa
                pass
            finally:
                print(project_root_path)

            # create docker process
            docker_client = docker.from_env()
            if project_language == 'python':
                container = docker_client.containers.run(
                    image='python:3.9',
                    command='sh -c "while true;do echo hello docker;sleep 1;done"',
                    volumes=[f'{project_root_path}:/{project_name}'],
                    detach=True,
                )

                docker_id = container.id

            new_project = Project(id=max_id + 1,
                                  creator_id=creator_id,
                                  create_time=datetime.date.fromtimestamp(time.time()),
                                  project_name=project_name,
                                  project_language=project_language,
                                  docker_id=docker_id)
            print(new_project.id)
            db.session.add(new_project)
            db.session.commit()
            return 'ok'
        except Exception as e:  # noqa
            print(e)
            return 'create project failed'

    def get_container_id(self, project_id: int):
        try:
            select_res = Project.query.filter_by(id=project_id).all()
            if len(select_res) == 0:
                return {"flag": False, "result": 'no such project id'}
            elif len(select_res) != 1:
                return {"flag": False, "result": 'unknown project id error'}

            target_project = select_res[0]
            return {"flag": True, "result": target_project.docker_id}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in get container id'}
