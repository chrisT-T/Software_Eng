from flask import Blueprint, send_file
from flask_restful import Api, Resource, abort, reqparse

from werkzeug.datastructures import FileStorage
from app.service.file import FileService

bp = Blueprint(
    "file",
    __name__
)

file_api = Api(bp)

file_service = FileService()

parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class File(Resource):
    def get(self, project_id, path):
        res, flag = file_service.download_file(path, project_id)
        if flag:
            return send_file(res), 200
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
        file = args['file']
        if not file:
            abort(400, message='No file available')
        res, flag = file_service.save_file(path, project_id, file)
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
