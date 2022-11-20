import json
import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User


class UserAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(username="test",
                  password_hash=generate_password_hash("test"))
        db.session.add(me)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_create_user(self):
        '''
        Test user post api
        '''
        with current_app.test_client() as cli:
            data = {"username": "adfwer", "password": "adfwer", "email": "a@126.com"}
            response = cli.post(
                "/api/user", data=data
            )
            self.assertEqual(json.loads(response.data)['message'], 'invalid argument: password')
            self.assertEqual(response.status_code, 400)

            data = {"username": "adfwer", "password": "Adfwer1!", "email": "a.com"}
            response = cli.post(
                "/api/user", data=data
            )
            self.assertEqual(json.loads(response.data)['message'], 'invalid argument: email')
            self.assertEqual(response.status_code, 400)

            data = {"username": "adfwer", "password": "Adfwer1!", "email": "a@126.com"}
            response = cli.post(
                "/api/user",
                data=data
            )
            json_data = json.loads(response.data)
            self.assertEqual(json_data, 2)
            self.assertEqual(response.status_code, 200)

            response = cli.post(
                "/api/user",
                data=data
            )
            json_data = json.loads(response.data)
            self.assertEqual(json_data['message'], "user exists")
            self.assertEqual(response.status_code, 400)

    def test_find_user(self):
        '''
        Test user get api
        '''
        data = {"username": "tttt"}
        response = current_app.test_client().get(
            f"/api/user?username={data['username']}",
        )
        self.assertEqual(response.status_code, 404)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "user not exist")

        data = {"username": "test"}
        response = current_app.test_client().get(
            f"/api/user?username={data['username']}",
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data, 1)
        self.assertEqual(response.status_code, 200)

        data = {"username": ""}
        response = current_app.test_client().get(
            f"/api/user?username={data['username']}",
        )
        print(response)
        print(response.data)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "bad arguments")
        self.assertEqual(response.status_code, 400)
