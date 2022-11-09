from re import compile, search

def check_create_user_param(content: dict):
    required_keys = ["username", "password", "email"]
    pat = [r"^[a-zA-Z0-9_-]{4,16}$", r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$", r'^(?=.{5,12}$)([a-zA-Z]+\d+)$']
    for key in required_keys:
        if not content(key):
            return key, False
    for i in range(len(required_keys)):
        if not search(pat[i], content[required_keys[i]]):
            return required_keys[i], False