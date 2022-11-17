from flask import Blueprint, send_file
from flask_login import login_required
from flask_restful import Api, Resource, abort, reqparse
from werkzeug.datastructures import FileStorage

from app.checker import check_project_permission
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
    @login_required
    def get(self, project_id, path):
        if not check_project_permission(project_id, 'read'):
            abort(404, message="Permission denied")
        res, flag = file_service.download_file(path, project_id)
        if flag:
            return send_file(res)
        else:
            abort(404, message=res)

    @login_required
    def post(self, project_id, path):
        if not check_project_permission(project_id, 'edit'):
            abort(400, message="Permission denied")
        res, flag = file_service.create_file(path, project_id)
        if flag:
            return '', 204
        else:
            abort(400, message=res)

    @login_required
    def put(self, project_id, path):
        if not check_project_permission(project_id, 'edit'):
            abort(404, message="Permission denied")
        args = parser.parse_args()
        file = args['file']
        if not file:
            abort(400, message='No file available')
        res, flag = file_service.save_file(path, project_id, file)
        if flag:
            return "", 204
        else:
            abort(400, message=res)

    @login_required
    def delete(self, project_id, path):
        if not check_project_permission(project_id, 'edit'):
            abort(404, message="Permission denied")
        res, flag = file_service.remove_file(path, project_id)
        if flag:
            return "", 204
        else:
            abort(404, message=res)


file_api.add_resource(File, "/api/file/<int:project_id>/<path:path>")
