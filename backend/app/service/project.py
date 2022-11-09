import datetime
import os
import time

import docker
from flask import current_app
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model.project import Project
from app.model import login


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
            return {"flag": True, "result": new_project.id}
        except Exception as e:  # noqa
            print(e)
            return {"flag": False, "result": 'create project failed'}

    def get_container_id(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}
            
            return {"flag": True, "result": target.docker_id}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in get container id'}
    
    def get_project(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": "no such project"}
            return {"flag": True, "result": target}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in get project'}
    def remove_project(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            db.session.delete(target)
            db.session.commit()
            return {"flag": True, "result": target.docker_id}
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in remove project'}
        
    def add_user_admin(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            user = login.User.query.filter_by(username=username).first()
            if user in target.admin_users:
                return {"flag": True, "result": "user already in admin list"}
            
            if user not in target.readonly_users and user not in target.editable_users:
                return {"flag": False, "result": "user not in project"}
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            target.admin_users.append(user)
            return {"flag": True, "result": "admin user added"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in add admin'}
        
    def add_user_read(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            user = login.User.query.filter_by(username=username).first()
            
            if user in target.readonly_users:
                return {"flag": True, "result": "user already in read list"}
            
            if user not in target.admin_users and user not in target.editable_users and user not in target.pending_users:
                return {"flag": False, "result": "user not in project"}
            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            if user in target.pending_users:
                target.pending_users.remove(user)
            target.readonly_users.append(user)
            return {"flag": True, "result": "read user added"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in add admin'}
        
    def add_user_edit(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            user = login.User.query.filter_by(username=username).first()
            
            if user in target.edit_users:
                return {"flag": True, "result": "user already in read list"}
            
            if user not in target.admin_users and user not in target.readonly_users:
                return {"flag": False, "result": "user not in project"}
            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            target.editable_users.append(user)
            return {"flag": True, "result": "edit user added"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in add admin'}
        
    def add_user_pending(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            user = login.User.query.filter_by(username=username).first()
            
            if user in target.edit_users or user in target.readonly_users or user in target.admin_users or user in target.pending_users:
                return {"flag": True, "result": "user already exist"}
            
            target.pending_users.append(user)
            return {"flag": True, "result": "pending user added"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in add admin'}
    
    def update_edit_time(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            target.last_edit_time = datetime.date.fromtimestamp(time.time())
            return {"flag": True, "result": "edit time updated"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in add admin'}
    
    def remove_user(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            user = login.User.query.filter_by(username=username).first()
            if not user:
                return {"flag": False, "result": 'no such user'}
            
            if user not in target.admin_users and user not in target.editable_users and user not in target.pending_users and user not in target.readonly_users:
                return {"flag": False, "result": 'user not exist in project'}
            
            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            if user in target.pending_users:
                target.pending_users.remove(user)
            return {"flag": True, "result": "user removed"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in remove user'}
        
    def change_name(self, project_id: int, name: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return {"flag": False, "result": 'no such project id'}

            target.name = name
            return {"flag": True, "result": "name changed"}
        
        except Exception as e:
            print(e)
            return {"flag": False, "result": 'Exception in remove user'}

    def to_dict(self, project: Project):
        return {
            "id": project.id,
            "project_name": project.project_name,
            "create_time": str(project.create_time),
            "last_edit_time": str(project.last_edit_time),
            "project_language": project.project_language,
            "creator_id": project.creator_id
        }