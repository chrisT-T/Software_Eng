from app.extensions import db
from app.model import project
from app.checker import check_create_project_param
from app.service import ProjectService
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)
service = ProjectService()


class Project(Resource):
    def get(self):

        project.Project.query.all()

        return "test"

    def post(self):
        content = request.get_json()
        if content is None:
            return {"message": "bad parameters"}
        key, passed = check_create_project_param(content)
        if passed:
            result = service.create_project(content['creator_id'], content['project_name'], content['project_language'])
            return {"message": result}
        else:
            return {"message": key}


api.add_resource(Project, '/api/project')
