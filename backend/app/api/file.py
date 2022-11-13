from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort

from app.service.file import FileService
bp = Blueprint(
    "file",
    __name__
)

file_api = Api(bp)

file_service = FileService()

parser = reqparse.RequestParser()
parser.add_argument('content', type=str)

class File(Resource):
    def get(self, project_id, path, filename):
        relative_path = path.replace("\\","/")
        res, flag = file_service.download_file(filename, relative_path, project_id)
        if flag:
            return res, 200
        else:
            abort(404, message=res)
    
    def post(self, project_id, path, filename):
        relative_path = path.replace("\\","/")
        
        res, flag = file_service.create_file(filename, relative_path, project_id)
        if flag:
            return res, 204
        else:
            abort(400, message=res)
            
    def put(self, project_id, path, filename):
        relative_path = relative_path = path.replace("\\","/")
        args = parser.parse_args()
        content = args['content']
        if not content:
            abort(400, message='No content available')
        res, flag = file_service.save_file(filename, relative_path, project_id, content)
        if flag:
            return res, 204
        else:
            abort(400, message=res)

file_api.add_resource(File, "/file/<int:project_id>/<str:path>/<str:filename>")