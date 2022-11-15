import os

from werkzeug.datastructures import FileStorage


from app.model.login import User
from app.model.project import Project


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
