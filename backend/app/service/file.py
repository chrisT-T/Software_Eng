import os

from app.model.project import Project
from app.model.login import User


class FileService():
    def create_file(self,
                    filename,
                    relative_path,
                    project_id):
        project = Project.query.filter_by(id=project_id).first()
        proj_path = project.path
        path = f'{proj_path}/{relative_path}/{filename}'
        if os.path.isfile(path):
            return "File already exists", False
        fp = open(path, 'w')
        fp.flush()
        fp.close()
        return '',  True
        
    def remove_file(self,
                    filename,
                    relative_path,
                    project_id):
        project = Project.query.filter_by(id=project_id).first()
        proj_path = project.path
        path = f'{proj_path}/{relative_path}/{filename}'
        if not os.path.isfile(path):
            return "File do not exist", False
        try:
            os.remove(path)
        except: #noqa
            pass
        
        return '',  True
    
    def save_file(self,
                  filename,
                  relative_path,
                  project_id,
                  content):
        project = Project.query.filter_by(id=project_id).first()
        proj_path = project.path
        path = f'{proj_path}/{relative_path}/{filename}'
        if not os.path.isfile(path):
            return "File do not exist", False
        with open(path, 'w') as fp:
            fp.write(content)
        return '',  True
    
    def download_file(self,
                      filename,
                      relative_path,
                      project_id):
        project = Project.query.filter_by(id=project_id).first()
        proj_path = project.path
        path = f'{proj_path}/{relative_path}/{filename}'
        if not os.path.isfile(path):
            return "File do not exist", False
        with open(path, 'r') as fp:
            content = fp.read()
        return content, True