from flask import Blueprint
from flask_restful import Api, Resource

from app.service import ProjectService

bp = Blueprint(
    "container",
    __name__
)

container_api = Api(bp)

project_service = ProjectService()


class Container(Resource):
    def get(self, project_id):
        res = project_service.get_container_id(project_id)
        if res["flag"]:
            return res["result"], 200
        else:
            return res["result"], 404


container_api.add_resource(Container, "/container/<int:project_id>")
