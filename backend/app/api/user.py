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
        username = request.args.get('username',None)
        if not username:
            return {'code': 1, 'message': 'bad arguments'}
        else:
            try:
                exist = service.find_user(username) 
                if exist:
                    return {'code': 1, 'message': 'user exists'}
                else:
                    return {'code': 0, 'message': 'user not exist'}
            except:
                return {'code': 0, 'message': 'user not exist'}

    def post(self):
        content = request.form.to_dict()
        print(content)
        if 'username' not in content.keys() or 'password' not in content.keys():
            return {'code': 401, 'message': 'bad arguments'}
        
        username = content['username']
        password = content['password']

        try:
            if (service.create_user(username, password)):
                return {'code': 200, 'message': "ok"}
            else:
                return {'code': 400, 'message': "user exists"}
        except:  # noqa
            return {'code': 401, "message": "create new user failed"}


user_api.add_resource(User, '/api/user')
