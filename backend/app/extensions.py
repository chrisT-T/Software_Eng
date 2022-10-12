from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_restful import Api

db = SQLAlchemy()
swagger = Swagger()
api = Api()
