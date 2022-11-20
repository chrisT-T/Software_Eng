from re import search


def check_create_user_param(content: dict):
    required_keys = ["username", "password", "email"]
    pat = [r"^[a-zA-Z0-9_-]{4,16}$",
           r'^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$',
           r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$"]
    for key in required_keys:
        if not content[key]:
            return key, False
    for i in range(len(required_keys)):
        if not search(pat[i], content[required_keys[i]]):
            return required_keys[i], False
    return "ok", True


def check_change_password_param(content: dict):
    required_keys = ["username", "password", "password_new"]
    for key in required_keys:
        if not content[key]:
            return key, False
    if content['password'] == content['password_new']:
        return 'password_new', False
    if not search(r'^.*(?=.{6,20})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$', content["password_new"]):
        return 'password_new', False
    return "ok", True
