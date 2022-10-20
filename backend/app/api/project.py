from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from app.extensions import db
from app.model import project

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)


class Project(Resource):
    def get(self):

        project.Project.query.all()

        return "test"


api.add_resource(Project, '/project')
