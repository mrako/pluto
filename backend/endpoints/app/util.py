import logging as log
from flask import current_app as app
from multiprocessing import Process, Queue


def github_auth_headers():
    return {'Authorization': 'Bearer '+app.config['GITHUB_ACCESS_TOKEN']}


def add_error(result, msg):
    result['success'] = False
    if 'errors' in result:
        result['errors'].append(msg)
    else:
        result['errors'] = [msg]


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, e: Exception):
    log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def query_db(result_field_name: str, dao_function, **kwargs):
    try:
        # Execute the dao method and return result
        return build_result(result_field_name, dao_function(**kwargs))
    except Exception as e:
        msg = f"Retrieving {result_field_name} failed"
        return build_error_result(msg, e)

