from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from json import dumps

from app.checker import check_create_project_param
from app.extensions import db
from app.model import project
from app.service import ProjectService, UserService

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)
proj_service = ProjectService()
user_service = UserService()

class Project(Resource):
    
    def get(self):
        project_id = request.args.get("id", None)
        if not project_id:
            return {'message': 'bad arguments'}, 400
        else:
            flag = proj_service.get_project(project_id)["flag"]
            if flag:
                proj = proj_service.get_project(project_id)['result']
                return {"message": dumps(proj,default=proj_service.to_dict)}, 200
            else:
                return {"message": "no such project"}, 404
            

    @login_required
    def post(self):
        content = request.get_json()
        if content is None:
            return {"message": "bad parameters"}, 400
        key, passed = check_create_project_param(content)
        if passed:
            user_result = user_service.find_user_by_id(id=content['creator_id'])
            if not user_result['flag']:
                return {"message": "Invalid User"}, 400
            user = user_result['result']
            if current_user.username == user.username:
                result = proj_service.create_project(content['creator_id'], content['project_name'], content['project_language'])
                return {"message": result}, 200
            else:
                return {"message": "Can't create project for other users"}
        else:
            return {"message": key}, 400


api.add_resource(Project, '/api/project')
