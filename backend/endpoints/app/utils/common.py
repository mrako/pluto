import logging as log
import json


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, e: Exception, log_exception=True):
    if log_exception:
        log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def build_result_from_dict(result_dict: dict):
    result = {"success": True} | result_dict
    return result


def get_boolean(value: str) -> bool:
    if value is True or (value == 'true' or value == 'True'):
        return True
    return False
