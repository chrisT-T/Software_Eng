import json
import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User
from app.model.project import Project


class UserAPITestCase(unittest.TestCase):
    coo = None
    def setUp(self):
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(username="test",
                  password_hash=generate_password_hash("test"))
        other = User(username='other',
                     password_hash=generate_password_hash('other'))
        proj = Project(
            project_name='test',
            project_language='python',
            creator_id=1,
            creator=me)
        proj.admin_users.append(me)
        db.session.add(me)
        db.session.add(proj)
        db.session.add(other)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_create_project(self):
        with current_app.test_client() as cli:
            login = {"username": "test", "password": "test"}
            response = cli.post(
                "/auth/login/",data=login
            )
            data = {"creator_id": 1, "project_name": "testProj", 'project_language': "python"}
            response = current_app.test_client().post(
                "/api/project/",
                data=data
            )
            self.assertEqual(response.status_code, 204)
            response = current_app.test_client().get(
                "/api/project/2"
            )
            name = json.loads(response.data)['project_name']
            self.assertEqual(name, "testProj")
        
        
    def test_get_project(self):
        with current_app.test_client() as cli:
            login = {"username": "test", "password": "test"}
            response = cli.post(
                "/auth/login/",data=login
            )
            response = current_app.test_client().get(
                "/api/project/1",
            )
            json_data = json.loads(response.data)
            self.assertEqual(json_data['project_name'], "test")
            self.assertEqual(response.status_code, 200)
        
    def test_remove_project(self):
        with current_app.test_client() as cli:
            login = {"username": "test", "password": "test"}
            response = cli.post(
                "/auth/login/",data=login
            )
            
            response = current_app.test_client().delete(
                "/api/project/1"
            )
            self.assertEqual(response.status_code, 204)
            
            response = current_app