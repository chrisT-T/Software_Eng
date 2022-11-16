from flask_login import current_user

from app.model.project import Project

def check_create_project_param(content: dict):
    required_keys = ['creator_id', 'project_name', 'project_language']
    for req_key in required_keys:
        if req_key not in content.keys():
            return req_key, False
    return 'ok', True

def check_project_permission(proj_id: int, perm: str="admin"):
    if not proj_id:
        return False
    username = current_user.username
    proj = Project.query.filter_by(id=proj_id).first()
    admins = proj.admin_users
    edits = proj.editable_users
    reads = proj.readonly_users
    if perm == "admin" or perm == "read" or perm == "edit":
        for admin in admins:
            if admin.username == username:
                return True
    elif perm == "read" or perm == "edit":
        for edit in edits:
            if edit.username == username:
                return True
    elif perm == "read":
        for read in reads:
            if read.username == username:
                return True
    return False