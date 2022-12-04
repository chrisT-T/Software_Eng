from flask_login import current_user

from app.model.project import Project
from app.service.user import UserService
from app.service.project import ProjectService

user_service = UserService()
proj_service = ProjectService()

def check_create_project_param(content: dict):
    '''
    check create project parameters

    :param content: should contain creator_id, project_name, project_language
    :type content: dict
    :return: if success, return ('ok', True), else, return (absence key, False)
    '''
    required_keys = ['creator_name', 'project_name', 'language']
    for req_key in required_keys:
        if req_key not in content.keys():
            return req_key, False
    return 'ok', True


def check_project_permission(proj_id: int, perm: str = "admin"):
    '''
    check the project permission of the current user by user name

    :param perm: the permission needed
    :type perm: str
    :return : bool
    '''
    if not proj_id:
        return False
    username = current_user.username
    proj = Project.query.filter_by(id=proj_id).first()
    if not proj:
        return False
    admins = proj.admin_users
    edits = proj.editable_users
    reads = proj.readonly_users
    if perm in ["admin", "read", "edit"]:
        for admin in admins:
            if admin.username == username:
                return True
    elif perm in ["read", "edit"]:
        for edit in edits:
            if edit.username == username:
                return True
    elif perm == "read":
        for read in reads:
            if read.username == username:
                return True
    return False


def check_edit_project_password(password: str):
    res, flag = user_service.find_user_by_username(current_user.username)
    if flag:
        return res.validate_password(password)
    return False

def check_change_user_permission_params(args, proj_id: int):
    params = ['original_permission', 'new_permission', 'username']
    for param in params:
        if not args[param]:
            return 'mission param: ' + param, False
    
    print(args)
    original_perm = args['original_permission']
    new_perm = args['new_permission']
    username = args['username']
    
    user, flag = user_service.find_user_by_username(username)
    if not flag:
        return 'user not exist', False
    
    proj, flag = proj_service.find_project(proj_id)
    if not flag: 
        return 'project not exist', False
    
    # special case: remove pending user
    if original_perm == 'pending' and new_perm == 'remove':
        if user not in proj.pending_users:
            return 'invalid origin permission', False
        else:
            return '', True
    
    # check original perm
    perms = ['admin', 'edit', 'read']
    if original_perm not in perms:
        return 'invalid origin permission', False
    
    groups = [proj.admin_users, proj.editable_users, proj.readonly_users]
    if user not in groups[perms.index(original_perm)]:
        return 'invalid origin permission', False
    
    # check new perm
    if new_perm not in ['admin', 'edit', 'read', 'remove']:
        return 'invalid new permission', False
    
    return '', True
    
def check_invite_user_params(args, proj_id:int):
    username = args['username']
    if not username:
        return 'missing param: username', False
    
    _, flag = user_service.find_user_by_username(username)
    if not flag:
        return 'user not exist', False
    
    _, flag = proj_service.find_project(proj_id)
    if not flag: 
        return 'project not exist', False
    
    return '', True