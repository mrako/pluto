import logging as log
import os


def success_result(message: str = None):
    result = {'success': True}
    if message is not None:
        result['message'] = message
    return result


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, exception: Exception = None):
    if exception is not None:
        log.error(message, exc_info=exception)
    return {"success": False, "errors": [message]}


def build_result_from_dict(result_dict: dict):
    result = {"success": True} | result_dict
    return result


def get_boolean(value: str) -> bool:
    if value is True or (value == 'true' or value == 'True'):
        return True
    return False
