import json
import unittest

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User
from app.model.project import Project


class DataBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(id=0, username="test", password_hash=generate_password_hash("test"))
        project1 = Project(project_name="proj", project_language="python", creator_id=0)
        project2 = Project(project_name="proj2", project_language="python", creator_id=0)
        db.session.add(me)
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()
    
    def test_relation(self):
        proj_list = Project.query.filter_by(creator_id=0).all()
        print(proj_list)
        self.assertEqual(len(proj_list), 2)