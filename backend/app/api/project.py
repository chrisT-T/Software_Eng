from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from app.model import project
from app.extensions import db

bp = Blueprint(
    'project',
    __name__
)

api = Api(bp)

class Project(Resource):
    def get(self):

        tmp = project.Project.query.all()

        return "test"

api.add_resource(Project, '/project')

