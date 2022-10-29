from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from app.extensions import db
from app.model import project
from app.service import UserService

service = UserService()

bp = Blueprint(
    'user',
    __name__
)

user_api = Api(bp)


class User(Resource):
    def get(self):
        content = request.get_json()
        
        if 'username' not in content.keys():
            return {'message': 'bad arguments'}
        else:
            try:
                exist = service.find_user(content["username"]) 
                if exist:
                    return {'message': 'user exists'}
                else:
                    return {'message': 'user not exist'}
            except:
                return {'message': 'user not exist'}

    def post(self):
        content = request.get_json()

        if 'username' not in content.keys() or 'password' not in content.keys():
            return {'message': 'bad arguments'}

        username = content['username']
        password = content['password']

        try:
            service.create_user(username, password)
            return {'message': "ok"}
        except:  # noqa
            return {"message": "create new user failed"}


user_api.add_resource(User, '/user')
