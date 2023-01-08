import os

from flask import current_app
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model.project import Project
from app.model.user import User
from app.service import ProjectService
from app.utils import config

app = create_app(os.getenv('TYPE', 'default'))
host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')
app.config['docker_config'] = config.get_yaml('docker')

print(app.config['docker_config'])
migrate = Migrate(app, db)


@app.cli.command("init_db")
def init_db():
    """Init db"""
    db.create_all()
    me = User(username="test",
              password_hash=generate_password_hash(str("test")))
    proj = Project(
        project_name="a",
        project_language="Python",
        docker_id="what",
        creator_id=1,
        creator=me)
    proj.admin_users.append(me)
    project_root_dir = (f'{hash(proj.create_time)}-{proj.project_name}-{proj.project_language}')
    rootdir = current_app.config['ROOT_DIR']
    proj.path = os.path.abspath(f'{rootdir}/{project_root_dir}')
    os.makedirs(proj.path)
    db.session.add(me)
    db.session.add(proj)
    me = User(username="test2",
              password_hash=generate_password_hash(str("test2")))
    proj = Project(
        project_name="a2",
        project_language="Python",
        docker_id="what2",
        creator_id=2,
        creator=me)
    proj.admin_users.append(me)
    project_root_dir = (f'{hash(proj.create_time)}-{proj.project_name}-{proj.project_language}')
    rootdir = current_app.config['ROOT_DIR']
    proj.path = os.path.abspath(f'{rootdir}/{project_root_dir}')
    os.makedirs(proj.path)
    db.session.add(me)
    db.session.add(proj)
    me = User(username="test3",
              password_hash=generate_password_hash(str("test3")))
    proj = Project(
        project_name="a3",
        project_language="Python",
        docker_id="what3",
        creator_id=3,
        creator=me)
    proj.admin_users.append(me)
    project_root_dir = (f'{hash(proj.create_time)}-{proj.project_name}-{proj.project_language}')
    rootdir = current_app.config['ROOT_DIR']
    proj.path = os.path.abspath(f'{rootdir}/{project_root_dir}')
    os.makedirs(proj.path)
    db.session.add(me)
    db.session.add(proj)
    me = User(username="test4",
              password_hash=generate_password_hash(str("test4")))
    proj = Project(
        project_name="a4",
        project_language="Python",
        docker_id="what4",
        creator_id=4,
        creator=me)
    proj.admin_users.append(me)
    project_root_dir = (f'{hash(proj.create_time)}-{proj.project_name}-{proj.project_language}')
    rootdir = current_app.config['ROOT_DIR']
    proj.path = os.path.abspath(f'{rootdir}/{project_root_dir}')
    os.makedirs(proj.path)
    db.session.add(me)
    db.session.add(proj)
    db.session.commit()


@app.cli.command("runserver")
def runserver():
    app.run(host=host, port=port)


if __name__ == '__main__':
    app.cli()
