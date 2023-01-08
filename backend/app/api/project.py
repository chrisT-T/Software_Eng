import os
import zipfile

from flask import Blueprint, current_app, json, request, send_file
from flask_login import current_user, login_required
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse

from app.checker import (check_change_user_permission_params,
                         check_create_project_param,
                         check_edit_project_password, check_invite_user_params,
                         check_project_permission)
from app.service import ProjectService, UserService

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)
proj_service = ProjectService()
user_service = UserService()

parser = reqparse.RequestParser()
parser.add_argument('creator_name', type=str, location='form')
parser.add_argument('project_name', type=str, location='form')
parser.add_argument('language', type=str, location='form', help='Bad choice: {error_msg}')
parser.add_argument('password', type=str, location='form')
parser.add_argument('new_name', type=str, location='form')
parser.add_argument('original_permission', type=str, location='form')
parser.add_argument('new_permission', type=str, location='form')
parser.add_argument('username', type=str, location='form')


class Project(Resource):
    res_fields = {
        "id": fields.Integer,
        "project_name": fields.String,
        "create_time": fields.String,
        "last_edit_time": fields.String,
        "project_language": fields.String,
        "creator_id": fields.Integer,
        "docker_id": fields.String,
        "hash_id": fields.String
    }

    @login_required
    @marshal_with(res_fields)
    def get(self, proj_id):
        """
        Get Project Info
        ---
        tags:
            - Project
        parameters:
            - name: project_id
              type: int
              required: true
              in: query
        responses:
            200:
                description: project dict
            400:
                description: no permission
            404:
                description: project doesn't exist

        """
        if not check_project_permission(proj_id, "read"):
            abort(400, message="Permission Denied")
        res, flag = proj_service.find_project(proj_id)
        if flag:
            return res, 200
        else:
            abort(404, message="Project {} doesn't exist".format(proj_id))

    @login_required
    def post(self):
        """
        Create project
        ---
        tags:
            - Project
        parameters:
            - name: project_name
              type: string
              required: true
              in: formData
            - name: language
              type: string
              required: true
              in: formData
        responses:
            400:
                description: failed, error in message
        """
        args = parser.parse_args()
        key, flag = check_create_project_param(args)
        if not flag:
            abort(400, message="Invalid argument {}".format(key))
        username = current_user.username
        user, flag = user_service.find_user_by_username(username)
        response, flag = proj_service.create_project(username, args['project_name'], args['language'])
        if flag:
            return response, 201
        else:
            abort(400, message=response)

    @login_required
    def put(self, proj_id):
        if not check_project_permission(proj_id, "edit"):
            abort(400, message="permission denied")
        args = parser.parse_args()
        password = args['password']
        new_name = args['new_name']
        print(args)
        if check_edit_project_password(password):
            res, flag = proj_service.change_name(proj_id, new_name)
            if flag:
                return res, 204
            else:
                abort(400, message=res)
        else:
            abort(401, message="password error")

    @login_required
    def delete(self, proj_id):
        """
        Delete Project
        ---
        tags:
            - Project
        parameters:
            - name: project_id
              type: int
              required: true
              in: query
            - name: password
              type: string
              required: true
              in: data
        responses:
            204:
                description: project delete success
            400:
                description: no permission
            401:
                description: invalid password
            404:
                description: project doesn't exist
            500:
                description: internal error

        """
        if not check_project_permission(proj_id, "admin"):
            abort(400, message="Permission denied")
        if not check_edit_project_password(json.loads(request.data)['password']):
            abort(401, message="invalid password")
        proj, flag = proj_service.find_project(proj_id)
        if flag:
            res, flag = proj_service.remove_project(proj_id)
            if flag:
                return '', 204
            else:
                abort(500, message=res)
        else:
            abort(404, message="Project {} doesn't exist".format(proj_id))


api.add_resource(Project, '/api/project/<int:proj_id>/', '/api/project/')


@bp.route('/api/project/<int:proj_id>/tree/', methods=['GET'])
@login_required
def file_tree(proj_id):
    if not check_project_permission(proj_id, "read"):
        return 'Permission denied', 401
    res, flag = proj_service.get_file_tree(proj_id)
    if flag:
        return res, 200
    else:
        return res, 400


@bp.route('/api/project/<int:proj_id>/perm/', methods=['POST'])
@login_required
def change_user_permission(proj_id):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401

    args = parser.parse_args()
    res, flag = check_change_user_permission_params(args, proj_id)

    if not flag:
        return res, 400

    original_perm = args['original_permission']
    new_perm = args['new_permission']
    username = args['username']
    flag = False
    if new_perm == 'remove':
        res, flag = proj_service.remove_user(proj_id, username, original_perm)
    else:
        res, flag = proj_service.change_user_permission(proj_id, username, original_perm, new_perm)
    if flag:
        return '', 204
    else:
        return res, 400


@bp.route('/api/project/<int:proj_id>/invite/', methods=['POST'])
@login_required
def invite_user(proj_id):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401
    args = parser.parse_args()
    res, flag = check_invite_user_params(args, proj_id)
    if not flag:
        return res, 400
    user = args['username']
    res, flag = proj_service.invite_user(proj_id, user)
    if not flag:
        return 'invite failed', 500
    return '', 204


@bp.route('/api/project/<int:proj_id>/download/', methods=['GET'])
@login_required
def download_project(proj_id):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401
    res, flag = proj_service.zip_project(proj_id)
    if not flag:
        return res, 500
    return send_file(res, as_attachment=True), 200


@bp.route('/api/project/<int:proj_id>/download/folder/<path:path>', methods=['GET'])
@login_required
def download_folder(proj_id, path):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401
    res, flag = proj_service.zip_folder(proj_id, path)
    if not flag:
        return res, 500
    return send_file(res, as_attachment=True), 200


@bp.route('/api/project/<int:proj_id>/download/single/<path:path>', methods=['GET'])
@login_required
def download_single(proj_id, path):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401
    project = proj_service.find_project(proj_id)[0]
    targetPath = os.path.join(project.path, path)
    return send_file(targetPath, as_attachment=True), 200


@bp.route('/api/project/<int:proj_id>/upload/single/<path:path>', methods=['POST'])
@login_required
def upload_single(proj_id, path):
    if not check_project_permission(proj_id, "admin"):
        return 'Permission denied', 401
    fileObj = request.files['file']
    project = proj_service.find_project(proj_id)[0]
    targetPath = os.path.join(project.path, path, fileObj.filename)
    fileObj.save(targetPath)
    return "upload success", 200


@bp.route('/api/project/upload/<string:username>/<string:name>/<string:language>', methods=['POST'])
@login_required
def upload_project(username, name, language):
    fileObj = request.files['file']
    print(username, name, language)
    new_proj_id, flag = proj_service.create_project(username, name, language)
    project = proj_service.find_project(new_proj_id)[0]
    targetPath = os.path.join(project.path, fileObj.filename)
    fileObj.save(targetPath)
    f = zipfile.ZipFile(targetPath, 'r')
    for file in f.namelist():
        f.extract(file, project.path)
    os.remove(targetPath)
    return "upload success", 200
