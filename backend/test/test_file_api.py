import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.user import User
from app.model.project import Project
from app.service.file import FileService
from app.service.project import ProjectService
from app.service.user import UserService

proj_service = ProjectService()
user_service = UserService()
file_service = FileService()


class FileAPITestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        user_service.create_user('test', 'test', 'a@126.com')
        proj_service.create_project(1, 'test', 'python')
        file_service.create_file('a.py', 1)

    def tearDown(self) -> None:
        proj_service.remove_project(1)
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_file(self):
        '''
        Test file post api
        '''
        with current_app.test_client() as cli:
            login = {"username": "test", "password": "test"}
            response = cli.post(
                "/login/", data=login
            )
            self.assertEqual(response.status_code, 204)

            response = cli.post("/api/file/1/folder/a.py")
            self.assertEqual(response.status_code, 204)

    # def test_remove_file(self):
    #     '''
    #     Test file delete api
    #     '''
    #     with current_app.test_client() as cli:
    #         login = {"username": "test", "password": "test"}
    #         response = cli.post(
    #             "/login/", data=login
    #         )
    #         self.assertEqual(response.status_code, 204)

    #         response = cli.delete("/api/file/1/a.py")
    #         self.assertEqual(response.status_code, 204)
    #         response = cli.get("/api/file/1/a.py")
    #         self.assertEqual(response.status_code, 404)
