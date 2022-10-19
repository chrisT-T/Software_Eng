import os
from flask_migrate import Migrate
from app import create_app
from app.utils import config
from app import db
from app.model.login import User
from werkzeug.security import generate_password_hash

app = create_app(os.getenv('TYPE', 'default'))
host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')

migrate = Migrate(app, db)


@app.cli.command("init_db")
def init_db():
    """Init db"""
    db.create_all()
    me = User(id=0, username="test",
              password_hash=generate_password_hash(str("test")))
    db.session.add(me)
    db.session.commit()


@app.cli.command("runserver")
def runserver():
    app.run()


if __name__ == '__main__':
    app.cli()
