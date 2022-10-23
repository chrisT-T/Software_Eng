from flask import Blueprint, jsonify

bp = Blueprint(
    'hello',
    __name__
)


@bp.route('/api/v1/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': "Hello world"}), 200
