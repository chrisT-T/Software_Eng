import json
import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User
from app.model.project import Project


class UserAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(id=1, username="test",
                  password_hash=generate_password_hash("test"))
        proj = Project(
            project_name='test',
            project_language='python',
            creator_id=1)
        proj.creator.append(me)
        db.session.add(me)
        db.session.add(proj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_create_project(self):
        login = {"username": "test", "password": "test"}
        current_app.test_client().post(
            "/auth/login",
            data=login
        )
        data = {"creator_id": 1, "project_name": "testProj", 'project_language': "python"}
        response = current_app.test_client().post(
            "/api/project",
            data=data
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['message'], "ok")
        self.assertEqual(response.status_code, 200)
        
    def test_get_project(self):
        response = current_app.test_client().get(
            "/api/project/1",
        )
        json_data = json.loads(response.data)
        self.assertEqual(json_data['project_name'], "test")
        self.assertEqual(response.status_code, 200)