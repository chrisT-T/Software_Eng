from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, abort

from app.checker import check_create_user_param
from app.extensions import db
from app.model import project
from app.service import UserService

service = UserService()

bp = Blueprint(
    'user',
    __name__
)

user_api = Api(bp)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str, location='form', required=True)
parser.add_argument('email', type=str, location='form')


class User(Resource):
    def get(self):
        args = parser.parse_args()
        username = args["username"]
        if not username:
            abort(400, message="bad arguments")
        else:
            try:
                flag = service.find_user_by_username(username)['flag']
                if flag:
                    abort(400, message="bad arguments")
                else:
                    return "", 204
            except Exception as e:
                abort(500, message=e)

    def post(self):
        args = parser.parse_args()
        key, flag = check_create_user_param(args)
        if not flag:
            abort(400, message="invalid arguments: {}".format(key))
        try:
            flag = service.create_user(args["username"], args["password"], args["email"])['flag']
            if (flag):
                return "", 204
            else:
                abort(400, message="user exists")
        except Exception as e:  # noqa
            print(e)
            abort(500, message="internal error")
        
    def patch(self):
        pass
    
    def put(self):
        pass


user_api.add_resource(User, '/api/user/')
