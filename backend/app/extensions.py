from flasgger import Swagger
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
swagger = Swagger()
api = Api()
login_manager = LoginManager()
csrf = CSRFProtect()
