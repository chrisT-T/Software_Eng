import datetime
import glob
import os
import time
from shutil import rmtree

import docker
from flask import current_app
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.model.project import Project
from app.model.user import User


class ProjectService():
    def create_project(self,
                       creator_name,
                       project_name,
                       project_language):
        '''
        create a project and create the corresponding docker container

        TODO: add docker run parameter to fit the traefik reverse-proxy
        return: ('Error Message', False) or ('new_project_id', True)
        '''
        try:
            creator = User.query.filter_by(username=creator_name).first()
            new_project = Project(creator_id=creator.id,
                                  project_name=project_name,
                                  project_language=project_language)
            new_project.admin_users.append(creator)

            hash_id = hash(new_project.create_time)

            # create project root_dir
            project_root_dir = (f'{hash_id}-{project_name}-{project_language}')
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
                    image='python_lsp:latest',
                    volumes=[f'{project_root_path}:/{project_name}'],
                    detach=True,
                    labels={
                        f"traefik.http.routers.{hash_id}-lsp.rule": f"Host(`{hash_id}.lsp.localhost`)",
                        f"traefik.http.routers.{hash_id}-lsp.service": f"{hash_id}-lsp-service",
                        f"traefik.http.services.{hash_id}-lsp-service.loadbalancer.server.port": "30000",
                        f"traefik.http.routers.{hash_id}-debug.rule": f"Host(`{hash_id}.debug.localhost`)",
                        f"traefik.http.routers.{hash_id}-debug.service": f"{hash_id}-debug-service",
                        f"traefik.http.services.{hash_id}-debug-service.loadbalancer.server.port": "30005",
                    },
                    network="traefik_default"
                )
                docker_id = container.id

            print(docker_id)
            new_project.docker_id = docker_id
            new_project.hash_id = hash_id
            db.session.add(new_project)
            db.session.commit()
            return new_project.id, True
        except Exception as e:  # noqa
            print(e)
            return 'create project failed', False

    def get_container_id(self, project_id: int):
        '''
        get docker container id by the corresponding project id

        :return: ("Error Message", False), (docker_id, True)
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            return target.docker_id, True
        except Exception as e:
            print(e)
            return 'Exception in get container id', False

    def get_project(self, project_id: int):
        '''
        get the project model instance by project id

        :return: ("Error Message", False), (project model, True)
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return "no such project", False
            return target, True
        except Exception as e:
            print(e)
            return 'Exception in get project', False

    def remove_project(self, project_id: int):
        '''
        remove project from database by project id

        :return: ("Error Message", False), ("", True)
        '''
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
        '''
        add a admin user to a project by project_id and username

        :return: ("Error Message", False), ("user already in admin list" or "admin user added", True),
        '''
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
        '''
        add a read user to a project by project_id and username

        :return: ("Error Message", False), ("user already in read list" or "read user added", True),
        '''
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
            return 'Exception in add read', False

    def add_user_edit(self, project_id: int, username: str):
        '''
        add a edit user to a project by project_id and username

        :return: ("Error Message", False), ("user already in edit list" or "edit user added", True),
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            user = User.query.filter_by(username=username).first()

            if user in target.edit_users:
                return "user already in edit list", True

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
        '''
        add a user to a project pending by project_id and username

        :return: ("Error Message", False), ("user already exist" or "pending user added", True),
        '''
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
            return 'Exception in add pending', False

    def update_edit_time(self, project_id: int):
        '''
        Update project edit time by the current backend time

        :return : ("Error Message", False) or ("edit time updated", True)
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False

            target.last_edit_time = datetime.date.fromtimestamp(time.time())
            return "edit time updated", True

        except Exception as e:
            print(e)
            return 'Exception in update edit time', False

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
        '''
        change project name
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            if not target:
                return 'no such project id', False
            target.project_name = name
            db.session.commit()
            return '', True
        except Exception as e:
            print(e)
            return 'Exception in remove user', False

    def get_file_data(self, src, project_rootdir):
        try:
            # print(src, current_app.config, os.path.join(current_app.config['ROOT_DIR'], src))
            isfile = os.path.isfile(src)
            current_node = {
                'label': os.path.basename(src),
                'path': os.path.relpath(src).replace(project_rootdir, ''),
                'type': 'file' if isfile else 'folder',
                'children': []
            }
            if current_node['path'] == '':
                current_node['path'] = '/'
            if isfile:
                return current_node
            else:
                child_files = glob.glob(os.path.abspath(src) + '/*')
                for child in child_files:
                    current_node['children'].append(self.get_file_data(child, project_rootdir))
                return current_node
        except Exception as e:
            print(e)
            return 'Exception in getting file tree', False

    def get_file_tree(self, proj_id: int):
        try:
            project = Project.query.filter_by(id=proj_id).first()
            project_abs_path = os.path.relpath(project.path)
            file_data = self.get_file_data(project_abs_path, project_abs_path)
            file_data['label'] = project.project_name
            return file_data, True
        except Exception as e:
            print(e)
            return 'Exception in getting file tree', False


if __name__ == '__main__':
    service = ProjectService()
    tmp = service.get_file_tree(6)
    print(tmp)
