import logging as log
from flask import current_app as app


def github_auth_headers():
    return {'Authorization': 'Bearer '+app.config['GITHUB_ACCESS_TOKEN']}


def add_error(result, msg):
    result['success'] = False
    if 'errors' in result:
        result['errors'].append(msg)
    else:
        result['errors'] = [msg]


def fail_with(msg):
    return {'success': False, 'errors': [msg]}


def query_db(field_name, func,  **kwargs):
    try:
        return {"success": True,
                field_name: func(**kwargs)}
    except:
        msg = f"Retrieving {field_name} failed"
        log.exception(msg)
        return {
            "success": False,
            "errors": [msg]
        }
