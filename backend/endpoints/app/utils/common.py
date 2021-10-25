import logging as log


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, e: Exception):
    log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def build_result_from_dict(result_dict: dict):
    result = {"success": True} | result_dict
    return result

