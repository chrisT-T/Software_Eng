
from flask import Blueprint, redirect, request, url_for
from flask_login import login_required

from app.checker import check_project_permission
from app.service.project import ProjectService
from app.service.user import UserService

bp = Blueprint('proj_service', __name__)

proj_service = ProjectService()
user_service = UserService()


@bp.route('/proj_service/tree/<int:proj_id>/', methods=['GET'])
@login_required
def tree(proj_id):
    if not check_project_permission(proj_id, "read"):
        return 'Permission denied', 400
    res, flag = proj_service.get_file_tree(proj_id)
    if flag:
        return res, 200
    else:
        return res, 400
