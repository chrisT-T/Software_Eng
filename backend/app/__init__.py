import os

from flask import Flask

from app.api import api_bp
from app.configs import configs
from app.extensions import api, csrf, db, login_manager, swagger


def init_extensions(app):
    db.init_app(app)
    swagger.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('TYPE', 'default')

    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    for bp in api_bp:
        app.register_blueprint(bp)

    init_extensions(app)
    return app
