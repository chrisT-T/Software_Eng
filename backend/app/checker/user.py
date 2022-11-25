import re


def check_create_user_param(content: dict):
    '''
    check the user parameters by regular expressions

    :param content: dict with keys: username, password, email 

    :return: (failed key, False) or ("ok", True)
    '''
    required_keys = ["username", "password", "email"]
    pat = [r"^[a-zA-Z0-9_-]{4,16}$",
           r'^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$',
           r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$"]
    for key in required_keys:
        if not content[key]:
            return key, False

    for pattern, key in zip(pat, required_keys):
        if not re.search(pattern, content[key]):
            return key, False
    return "ok", True


def check_change_password_param(content: dict):
    '''
    checker in the update password process

    note: if password_new == password and password_new invaild, return (password_new, False)

    :param content: dict with keys: username, password, password_new
    :return: (failed key, False) or "ok" True
    '''
    required_keys = ["username", "password", "password_new"]
    for key in required_keys:
        if not content[key]:
            return key, False
    if content['password'] == content['password_new']:
        return 'password_new', False
    if not re.search(r'^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$', content["password_new"]):
        return 'password_new', False
    return "ok", True
