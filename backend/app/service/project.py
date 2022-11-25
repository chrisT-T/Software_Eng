import datetime
import os
import time
from pathlib import Path
from shutil import rmtree

import docker
from flask import current_app
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model.user import User
from app.model.project import Project


class ProjectService():
    def create_project(self,
                       creator_name,
                       project_name,
                       project_language):
        try:
            creator = User.query.filter_by(username=creator_name).first()
            new_project = Project(creator_id=creator.id,
                                  project_name=project_name,
                                  project_language=project_language)
            new_project.admin_users.append(creator)

            # create project root_dir
            project_root_dir = (f'{hash(new_project.create_time)}-{project_name}-{project_language}')
            rootdir = current_app.config['ROOT_DIR']
            project_root_path = os.path.join(rootdir, project_root_dir)
            project_root_path = os.path.abspath(project_root_path)
            if not os.path.exists(project_root_path):
                os.makedirs(project_root_path)
            new_project.path = project_root_path

            # create docker process
            docker_client = docker.from_env()
            if project_language == 'Python':
                container = docker_client.containers.run(
                    image='python:3.9',
                    command='sh -c "while true;do echo hello docker;sleep 1;done"',
                    volumes=[f'{project_root_path}:/{project_name}'],
                    detach=True,
                )
                docker_id = container.id
            print(docker_id)
            new_project.docker_id = docker_id

            db.session.add(new_project)
            db.session.commit()
            return new_project.id, True
        except Exception as e:  # noqa
            print(e)
            return 'create project failed', False

    def get_container_id(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            return target.docker_id, True
        except Exception as e:
            print(e)
            return 'Exception in get container id', False

    def get_project(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return "no such project", False
            return target, True
        except Exception as e:
            print(e)
            return 'Exception in get project', False

    def remove_project(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'project {project_id} does not exist', False
            docker_id = target.docker_id
            docker_client = docker.from_env()
            container = docker_client.containers.get(docker_id)
            container.kill()
            container.remove()
            rmtree(target.path)
            db.session.delete(target)
            db.session.commit()
            return '', True
        except Exception as e:
            print(e)
            return 'Exception in remove project', False

    def add_user_admin(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()
            if user in target.admin_users:
                return "user already in admin list", True

            if user not in target.readonly_users and user not in target.editable_users:
                return "user not in project", False
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            target.admin_users.append(user)
            return "admin user added", True

        except Exception as e:
            print(e)
            return 'Exception in add admin', False

    def add_user_read(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()

            if user in target.readonly_users:
                return "user already in read list", True

            if user not in target.admin_users and user not in target.editable_users and user not in target.pending_users:
                return "user not in project", False
            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            if user in target.pending_users:
                target.pending_users.remove(user)
            target.readonly_users.append(user)
            return "read user added", True

        except Exception as e:
            print(e)
            return 'Exception in add admin', False

    def add_user_edit(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()

            if user in target.edit_users:
                return "user already in read list", True

            if user not in target.admin_users and user not in target.readonly_users:
                return "user not in project", False
            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            target.editable_users.append(user)
            return "edit user added", True

        except Exception as e:
            print(e)
            return 'Exception in add admin', False

    def add_user_pending(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()

            if user in target.edit_users or user in target.readonly_users or user in target.admin_users or user in target.pending_users:
                return "user already exist", True

            target.pending_users.append(user)
            return "pending user added", True

        except Exception as e:
            print(e)
            return 'Exception in add admin', False

    def update_edit_time(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            target.last_edit_time = datetime.date.fromtimestamp(time.time())
            return "edit time updated", True

        except Exception as e:
            print(e)
            return 'Exception in add admin', False

    def remove_user(self, project_id: int, username: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()
            if not user:
                return 'no such user', False

            if user not in target.admin_users and user not in target.editable_users and user not in target.pending_users and user not in target.readonly_users:
                return 'user not exist in project', False

            if user in target.admin_users:
                target.admin_users.remove(user)
            if user in target.readonly_users:
                target.readonly_users.remove(user)
            if user in target.editable_users:
                target.editable_users.remove(user)
            if user in target.pending_users:
                target.pending_users.remove(user)
            return "user removed", True

        except Exception as e:
            print(e)
            return 'Exception in remove user', False

    def change_name(self, project_id: int, name: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            target.name = name
            return "name changed", True

        except Exception as e:
            print(e)
            return 'Exception in remove user', False

    def get_file_tree(self, project_id: int):
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False
            p = Path(target.path)
            path_list = [str(i) for i in p.rglob('*')]
            return path_list, True

        except Exception as e:
            print(e)
            return 'Exception in getting file tree', False
