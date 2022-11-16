from functools import wraps

from flask_login import current_user

from app.model.project import Project

def permission_required(proj_id: int, perm: str="admin"):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            username = current_user.username
            proj = Project.query.filter_by(id=proj_id).first()
            admins = proj.admin_users
            edits = proj.editable_users
            reads = proj.readonly_users
            if perm == "admin" or perm == "read" or perm == "edit":
                for admin in admins:
                    if admin.username == username:
                        func(*args, **kwargs)
                        return
            elif perm == "read" or perm == "edit":
                for edit in edits:
                    if edit.username == username:
                        func(*args, **kwargs)
                        return
            elif perm == "read":
                for read in reads:
                    if read.username == username:
                        func(*args, **kwargs)
                        return
        return wrapped_func
    return decorator