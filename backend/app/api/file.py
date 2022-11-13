from flask import Blueprint
from flask_restful import Api, Resource

bp = Blueprint(
    "file",
    __name__
)

file_api = A