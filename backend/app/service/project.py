import datetime
import glob
import os
import time
import zipfile
from shutil import rmtree

import docker
from flask import current_app

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

            if project_language not in current_app.config['docker_config'].keys():
                print(f"wrong project language {project_language}")
                return f"wrong project language {project_language}", False

            image_tag = current_app.config['docker_config'][project_language]

            container = docker_client.containers.run(
                image=image_tag,
                volumes=[f'{project_root_path}:/{project_name}'],
                detach=True,
                labels={
                    f"traefik.http.routers.{hash_id}-lsp.rule": f"Path(`/lsp/{hash_id}`)",
                    f"traefik.http.routers.{hash_id}-lsp.service": f"{hash_id}-lsp-service",
                    f"traefik.http.services.{hash_id}-lsp-service.loadbalancer.server.port": "30000",
                    f"traefik.http.routers.{hash_id}-debug.rule": f"Path(`localhost/debug/{hash_id}`)",
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

    def find_project(self, project_id: int):
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

    def change_user_permission(self, project_id: int, username: str, original_perm: str, new_perm: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            user = User.query.filter_by(username=username).first()

            perms = ['admin', 'edit', 'read']
            groups = [target.admin_users, target.editable_users, target.readonly_users]

            groups[perms.index(original_perm)].remove(user)
            groups[perms.index(new_perm)].append(user)
            db.session.commit()

            return "permission changed", True

        except Exception as e:
            print(e)
            return 'Exception in changing permission', False

    def invite_user(self, project_id: int, username: str):
        '''
        add a user to a project pending by project_id and username

        :return: ("Error Message", False), ("user already exist" or "pending user added", True),
        '''
        try:
            target = Project.query.filter_by(id=project_id).first()
            user = User.query.filter_by(username=username).first()

            if user in target.editable_users or user in target.readonly_users or user in target.admin_users or user in target.pending_users:
                return "user already exist", False

            target.pending_users.append(user)
            db.session.commit()
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
            target.last_edit_time = datetime.date.fromtimestamp(time.time())

            return "edit time updated", True

        except Exception as e:
            print(e)
            return 'Exception in update edit time', False

    def remove_user(self, project_id: int, username: str, original_perm: str):
        try:
            target = Project.query.filter_by(id=project_id).first()
            user = User.query.filter_by(username=username).first()

            perms = ['admin', 'edit', 'read', 'pending']
            groups = [target.admin_users, target.editable_users, target.readonly_users, target.pending_users]

            groups[perms.index(original_perm)].remove(user)

            db.session.commit()
            return "user removed", True

        except Exception as e:
            print(e)
            return 'Exception in remove user', False

    def accept_invitation(self, username, proj_id):
        try:
            target = Project.query.filter_by(id=proj_id).first()
            user = User.query.filter_by(username=username).first()

            target.pending_users.remove(user)
            target.readonly_users.append(user)
            db.session.commit()

            return "invitation accepted", True

        except Exception as e:
            print(e)
            return 'Exception in accepting invitation', False

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

    def zip_project(self, proj_id: int):
        try:
            project = Project.query.filter_by(id=proj_id).first()
            project_abs_path = os.path.relpath(project.path)
            zip_folder_path = os.path.join(os.path.dirname(project_abs_path), 'tmpZip')
            zip_path = os.path.join(os.path.dirname(project_abs_path), 'tmpZip', project.project_name + '.zip')
            print(zip_folder_path)
            if not os.path.exists(zip_folder_path):
                os.makedirs(zip_folder_path)
            zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            for path, dirnames, filenames in os.walk(project_abs_path):

                fpath = path.replace(project_abs_path, '')
                for filename in filenames:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip.close()
            return '../' + zip_path, True
        except Exception as e:
            print(e)
            return 'Exception in zipping files', False

    def zip_folder(self, proj_id: int, path: str):
        try:
            project = Project.query.filter_by(id=proj_id).first()
            project_abs_path = os.path.relpath(os.path.join(project.path, path))
            path_string = os.path.join(project.project_name, path).replace('/', '-')

            tmp_path = os.path.join(os.path.dirname(os.path.relpath(project.path)), 'tmpZip')

            zip_path = os.path.join(tmp_path, path_string + '.zip')
            if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
            zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)

            for path, dirnames, filenames in os.walk(project_abs_path):
                fpath = path.replace(project_abs_path, '')
                for filename in filenames:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip.close()
            return '../' + zip_path, True
        except Exception as e:
            print(e)
            return 'Exception in zipping files', False
