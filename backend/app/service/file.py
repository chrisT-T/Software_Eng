import os

from werkzeug.datastructures import FileStorage

from app.model.project import Project
from app.model.user import User


class FileService():
    def create_file(self,
                    relative_path,
                    project_id):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False

        path = os.path.join(project.path, relative_path)
        if os.path.isfile(path):
            return "File already exists", False

        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        open(path, 'x').close()
        return '', True

    def remove_file(self,
                    relative_path,
                    project_id):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False
        proj_path = project.path
        path = os.path.join(proj_path, relative_path)
        if not os.path.isfile(path):
            return "File do not exist", False
        try:
            os.remove(path)
        except:  # noqa
            pass

        return '', True

    def save_file(self,
                  relative_path,
                  project_id,
                  file: FileStorage):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False
        proj_path = project.path
        path = os.path.join(proj_path, relative_path)
        if not os.path.isfile(path):
            return "File do not exist", False
        os.remove(path)
        file.save(path)
        return '', True

    def download_file(self,
                      relative_path,
                      project_id):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False
        proj_path = project.path
        path = os.path.join(proj_path, relative_path)
        if not os.path.isfile(path):
            return "File do not exist", False
        return path, True

    def create_dir(self, relative_path, project_id):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False
        proj_path = project.path
        path = os.path.join(proj_path, relative_path)
        if os.path.exists(path):
            return "Folder already exists", False
        os.mkdir(path)
        return '', True
    
    def rename_file(self, relative_path, project_id, new_name):
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return 'Project does not exist', False
        proj_path = project.path
        path = os.path.join(proj_path, relative_path)
        if not (os.path.isfile(path) or os.path.isdir(path)):
            return "File or folder do not exist", False
        folder = os.path.dirname(path)
        os.rename(path, os.path.join(folder, new_name))
        return '', True