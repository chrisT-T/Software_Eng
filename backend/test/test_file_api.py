import json
import unittest
import datetime
import time

from flask import current_app, url_for
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User
from app.model.project import Project

class FileAPITestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.app = create_app('test')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        me = User(id=0, username="test",
                  password_hash=generate_password_hash("test"))
        proj = Project(
            project_name="a",
            create_time=datetime.date.fromtimestamp(time.time()),
            last_edit_time=datetime.date.fromtimestamp(time.time()),
            project_language="python",
            docker_id="what",
            creator_id=1,
            creator=me)
        db.session.add(me)
        db.session.add(proj)
        db.session.commit()

        db.session.commit()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_create_file(self):
        '''
        Test create_file api
        '''
        pass