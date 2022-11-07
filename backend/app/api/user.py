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
        username = request.args.get('username', None)
        if not username:
            return {'message': 'bad arguments'}, 400
        else:
            try:
                user = service.find_user(username)
                if user:
                    return {'message': 'user exists'}, 200
                else:
                    return {'message': 'user not exist'}, 204
            except Exception:
                return {'message': 'user not exist'}, 500

    def post(self):
        content = request.form.to_dict()
        print(content)
        if 'username' not in content.keys() or 'password' not in content.keys():
            return {'message': 'bad arguments'}, 400

        username = content['username']
        password = content['password']

        try:
            if (service.create_user(username, password)):
                return {'message': "ok"}, 201
            else:
                return {'message': "user exists"}, 400
        except:  # noqa
            return {"message": "create new user failed"}, 500


user_api.add_resource(User, '/api/user')
