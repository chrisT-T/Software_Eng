from flask import Blueprint, request
from flask_login import current_user, login_required
from flask_restful import Api, Resource, abort, reqparse

from app.checker import (check_change_password_param, check_create_user_param,
                         check_project_permission)
from app.service import ProjectService, UserService

user_service = UserService()
proj_service = ProjectService()
bp = Blueprint(
    'user',
    __name__
)

user_api = Api(bp)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, location=['args', 'form'])
parser.add_argument('password', type=str, location='form')
parser.add_argument('password_new', type=str, location='form')
parser.add_argument('email', type=str, location='form')


class User(Resource):
    def get(self):
        """
        Get User
        ---
        tags:
            - User
        parameters:
            - name: username
              type: string
              required: true
              in: query
        responses:
            200:
                description: user id of the given username
            404:
                description: bad arguments
            404:
                description: user does not exit
        """
        args = parser.parse_args()
        username = args["username"]
        if not username:
            abort(400, message="bad arguments")
        res, flag = user_service.find_user_by_username(username)
        if flag:
            # TODO: add field
            return res.id, 200
        else:
            abort(404, message="user not exist")

    def post(self):
        """
        Create new user
        ---
        tags:
            - User
        parameters:
            - name: username
              type: string
              required: true
              in: formData
            - name: password
              type: string
              required: true
              in: formData
            - name: email
              type: string
              required: true
              in: formData
        responses:
            200:
                description: id of created user
            400:
                description: invalid argument or user has been exits
        """
        args = parser.parse_args()
        key, flag = check_create_user_param(args)
        if not flag:
            abort(400, message="invalid argument: {}".format(key))
        id, flag = user_service.create_user(args["username"], args["password"], args["email"])
        if flag:
            return id, 201
        else:
            abort(400, message="user exists")

    def patch(self):  # patch is designed for resetting password
        """
        Reset user password
        ---
        tags:
            - User
        parameters:
            - name: username
              type: string
              required: true
              in: formData
            - name: password
              type: string
              required: true
              in: formData
            - name: password_new
              type: string
              required: true
              in: formData
        responses:
            200:
                description:
            400:
                description: invalid argument or user has been exits
        """
        args = parser.parse_args()
        key, flag = check_change_password_param(args)
        if not flag:
            abort(400, message="invalid argument: {}".format(key))

        user, flag = user_service.find_user_by_username(args['username'])
        if not user.validate_password(args['password']):
            abort(400, message="invalid password")
        user.set_password(args['password_new'])

    def put(self):  # put is designed for changing data
        pass


user_api.add_resource(User, '/api/user')


@bp.route('/api/user/<string:username>/projects/', methods=['GET'])
@login_required
def related_projects(username):
    res, flag = user_service.find_user_by_username(username)
    if not flag:
        abort(400, message=res)
    admins = res.admin_projects
    edits = res.editable_projects
    reads = res.readonly_projects
    response = []
    for i in admins + edits + reads:
        perm_name = []
        for user in i.readonly_users:
            perm_name.append({
                'user': user.username,
                'permission': 'readonly',
            })
        for user in i.editable_users:
            perm_name.append({
                'user': user.username,
                'permission': 'edit',
            })
        for user in i.admin_users:
            perm_name.append({
                'user': user.username,
                'permission': 'administrator',
            })
        for user in i.pending_users:
            perm_name.append({
                'user': user.username,
                'permission': 'pending',
            })
        response.append({
            'projectID': i.id,
            'projectName': i.project_name,
            'language': i.project_language,
            'creator': i.creator.username,
            'permissionGp': perm_name,
            'lastUpdateTime': i.last_edit_time,
            'createTime': i.create_time,
            'dockerId': i.docker_id
        })
    return response, 200
