from flask import Blueprint, request
from flask_login import current_user, login_required
from flask_restful import Api, Resource, abort, reqparse

from app.checker import check_change_password_param, check_create_user_param
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
parser.add_argument('username', type=str, location=['args', 'form'])
parser.add_argument('password', type=str, location='form')
parser.add_argument('password_new', type=str, location='form')
parser.add_argument('email', type=str, location='form')


class User(Resource):
    def get(self):
        args = parser.parse_args()
        username = args["username"]
        if not username:
            abort(400, message="bad arguments")
        res, flag = service.find_user_by_username(username)
        if flag:
            return res.id, 200
        else:
            abort(404, message="user not exist")
            
    def post(self):
        args = parser.parse_args()
        key, flag = check_create_user_param(args)
        if not flag:
            abort(400, message="invalid argument: {}".format(key))
        id, flag = service.create_user(args["username"], args["password"], args["email"])
        print(flag)
        if flag:
            return id, 200
        else:
            abort(400, message="user exists")

    def patch(self):  # patch is designed for resetting password
        args = parser.parse_args()
        key, flag = check_change_password_param(args)
        if not flag:
            abort(400, message="invalid argument: {}".format(key))

        user, flag = service.find_user_by_username(args['username'])
        if not user.validate_password(args['password']):
            abort(400, message="invalid password")
        user.set_password(args['password_new'])

    def put(self):  # put is designed for changing data
        pass


user_api.add_resource(User, '/api/user')
