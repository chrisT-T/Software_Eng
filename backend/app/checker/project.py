def check_create_project_param(content: dict):
    required_keys = ['creator_id', 'project_name', 'project_language']
    for req_key in required_keys:
        if req_key not in content.keys():
            return req_key, False
    return 'ok', True
