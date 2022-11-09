import os
import datetime
import time

from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.login import User
from app.utils import config
from app.model.project import Project

app = create_app(os.getenv('TYPE', 'default'))
host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')

migrate = Migrate(app, db)


@app.cli.command("init_db")
def init_db():
    """Init db"""
    db.create_all()
    me = User(username="test",
              password_hash=generate_password_hash(str("test")))
    proj = Project(
        project_name="a", 
        create_time=datetime.date.fromtimestamp(time.time()), 
        last_edit_time=datetime.date.fromtimestamp(time.time()), 
        project_language="python",
        docker_id="what",
        creator_id=0,
        creator=me)
    proj.admin_users.append(me)
    db.session.add(me)
    db.session.add(proj)
    db.session.commit()


@app.cli.command("runserver")
def runserver():
    app.run()


if __name__ == '__main__':
    app.cli()
