from flask import Blueprint, current_app
from flask_login import current_user, login_required
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse

from app.checker import check_create_project_param, check_project_permission
from app.service import ProjectService, UserService

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)
proj_service = ProjectService()
user_service = UserService()

parser = reqparse.RequestParser()
parser.add_argument('creator_id', type=int, location='form')
parser.add_argument('project_name', type=str, location='form')
parser.add_argument('project_language', type=str, location='form', choices=('python', 'cpp', 'typescript'), help='Bad choice: {error_msg}')


class Project(Resource):
    res_fields = {
        "id": fields.Integer,
        "project_name": fields.String,
        "create_time": fields.String,
        "last_edit_time": fields.String,
        "project_language": fields.String,
        "creator_id": fields.Integer
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
        res, flag = proj_service.get_project(proj_id)
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
            - name: creator_id
              type: int
              required: true
              in: formData
            - name: project_name
              type: string
              required: true
              in: formData
            - name: project_language
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
        user, flag = user_service.find_user_by_id(args['creator_id'])
        if not flag:
            abort(400, message="User {} not exist".format(args['creator_id']))
        if current_user.username == user.username:
            response, flag = proj_service.create_project(args['creator_id'], args['project_name'], args['project_language'])
            if flag:
                return response, 200
            else:
                abort(400, message=response)
        else:
            abort(400, message="Can't create project for other users")

    @login_required
    def put(self, proj_id):
        if check_project_permission(proj_id, "edit"):
            pass

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
        responses:
            204:
                description: project delete success
            400:
                description: no permission
            404:
                description: project doesn't exist
            500:
                description: delete project failed

        """
        if not check_project_permission(proj_id, "admin"):
            abort(400, message="Permission denied")
        proj, flag = proj_service.get_project(proj_id)
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
def tree(proj_id):
    if not check_project_permission(proj_id, "read"):
        return 'Permission denied', 400
    res, flag = proj_service.get_file_tree(proj_id)
    if flag:
        return res, 200
    else:
        return res, 400
