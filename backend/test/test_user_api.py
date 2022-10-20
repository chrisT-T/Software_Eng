import json
import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(id=0, username="test",
                  password_hash=generate_password_hash("test"))
        db.session.add(me)
        db.session.commit()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_create_user(self):
        '''
        Test create_user api
        '''
        data = {"username": "adfwer", "password": "adfwer"}
        response = current_app.test_client().post(
            "/user",
            json=data
        )

        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

        data = {"username": "abcd", "password": "abcd"}
        response = current_app.test_client().post(
            "/user",
            json=data
        )

        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        data = {"creator_id": 0, "project_name": "testProj", 'project_language': "python"}
        response = current_app.test_client().post(
            "/project",
            json=data
        )

        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
