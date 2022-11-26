from flask import Blueprint, json, request, send_file
from flask_login import login_required
from flask_restful import Api, Resource, abort, reqparse
from werkzeug.datastructures import FileStorage

from app.checker import check_project_permission
from app.extensions import swagger
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
        """
        Download File
        ---
        tags:
            - File
        parameters:
            - name: project_id
              in: path
              required: true
              type: int
            - name: path
              in: path
              required: true
              type: string
        responses:
            200:
                description: send file success
            401:
                description: check permission denied
            404:
                description: send file failed
        """
        if not check_project_permission(project_id, 'read'):
            abort(401, message="Permission denied")
        res, flag = file_service.download_file(path, project_id)
        if flag:
            return send_file(res)
        else:
            abort(404, message=res)

    @login_required
    def post(self, project_id, path):
        """
        Create new File
        ---
        tags:
            - File
        parameters:
            - name: project_id
              in: path
              required: true
              type: int
            - name: path
              in: path
              required: true
              type: string
            - name: type
              in: formData
              required: true
              type: string
        responses:
            204:
                description: upload success
            400:
                description: Permission denied or upload failed
        """
        type = json.loads(request.data)['type']
        if not type:
            abort(400, message='invalid arguments')
        if not check_project_permission(project_id, 'edit'):
            abort(400, message="Permission denied")
        if type == 'folder':
            res, flag = file_service.create_dir(path, project_id)
            if flag:
                return '', 201
            else:
                abort(400, message=res)
        else:
            res, flag = file_service.create_file(path, project_id)
            if flag:
                return '', 201
            else:
                abort(400, message=res)

    @login_required
    def put(self, project_id, path):
        """
        Upload File
        ---
        tags:
            - File
        parameters:
            - name: project_id
              in: path
              required: true
              type: int
            - name: path
              in: path
              required: true
              type: string
        responses:
            204:
                description: create file success
            400:
                description: No file available
            404:
                description: Permission denied or upload failed
        """
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
        """
        Delete File
        ---
        tags:
            - File
        parameters:
            - name: project_id
              in: path
              required: true
              type: int
            - name: path
              in: path
              required: true
              type: string
        responses:
            204:
                description: delete success
            404:
                description: Permission denied or delete failed
        """
        if not check_project_permission(project_id, 'edit'):
            abort(404, message="Permission denied")
        res, flag = file_service.remove_file(path, project_id)
        if flag:
            return "", 204
        else:
            abort(404, message=res)


file_api.add_resource(File, "/api/file/<int:project_id>/<path:path>")
