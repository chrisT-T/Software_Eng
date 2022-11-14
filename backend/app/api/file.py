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
    def get(self, project_id, path):
        res, flag = file_service.download_file(path, project_id)
        if flag:
            return res, 200
        else:
            abort(404, message=res)
    
    def post(self, project_id, path):
        res, flag = file_service.create_file(path, project_id)
        if flag:
            return '', 204
        else:
            abort(400, message=res)
            
    def put(self, project_id, path):
        args = parser.parse_args()
        content = args['content']
        if not content:
            abort(400, message='No content available')
        print(content)
        res, flag = file_service.save_file(path, project_id, content)
        if flag:
            return res, 204
        else:
            abort(400, message=res)
    
    def delete(self, project_id, path):
        res, flag = file_service.remove_file(path, project_id)
        if flag:
            return res, 200
        else:
            abort(404, message=res)
            
file_api.add_resource(File, "/file/<int:project_id>/<path:path>")