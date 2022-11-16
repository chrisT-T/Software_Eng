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
    def __init__(self):
        
        super().__init__()
    
    @login_required
    @marshal_with(res_fields)
    def get(self, proj_id): 
        if check_project_permission(proj_id, "read"):
            res, flag = proj_service.get_project(proj_id)
            if flag:
                return res, 200
            else:
                abort(404, message="Project {} doesn't exist".format(proj_id))

    @login_required
    def post(self):
        args = parser.parse_args()
        key, passed = check_create_project_param(args)
        if passed:
            user, flag = user_service.find_user_by_id(args['creator_id'])
            if not flag:
                abort(400, message="User {} not exist".format(args['creator_id']))
            if current_user.username == user.username:
                response, flag = proj_service.create_project(args['creator_id'], args['project_name'], args['project_language'])
                if flag:
                    return "", 204
                else:
                    abort(400, message=response)
            else:
                abort(400, message="Can't create project for other users")
        else:
            abort(400, message="Invalid argument {}".format(key))

    @login_required
    def put(self, proj_id):
        if check_project_permission(proj_id, "edit"):
            pass

    @login_required
    def delete(self, proj_id):
        if check_project_permission(proj_id, "admin"):
            proj, flag = proj_service.get_project(proj_id)
            if flag:
                admins = proj.admin_users
                flag = False
                for admin in admins:
                    if admin.username == current_user.username:
                        flag = True
                if flag:
                    res, flag = proj_service.remove_project(proj_id)
                    if flag:
                        return '', 204
                    else:
                        abort(500, message=res)
                else:
                    abort(400, message="Permission denied")
            else:
                abort(404, message="Project {} doesn't exist".format(proj_id))


api.add_resource(Project, '/api/project/<int:proj_id>', '/api/project/')
