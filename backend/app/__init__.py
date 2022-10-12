from flask import Flask

def create_app(config_name=None):
    app = Flask(__name__)
    return app
