import logging as log
import os


def success_result(message: str = None, status_code: int = 200):
    result = {'success': True, 'status_code': status_code}
    if message is not None:
        result['message'] = message
    return result


def build_result(result_field_name: str, response, status_code: int = 200):
    result = success_result(status_code=status_code)
    result[result_field_name] = response
    return result


def build_error_result(message: str, status_code: int = 500, exception: Exception = None):
    if exception is not None:
        log.error(message, exc_info=exception)
    return {"success": False, "status_code": status_code, "errors": [message]}


def build_result_from_dict(result_dict: dict, status_code: int = 200):
    return success_result(status_code=status_code) | result_dict


def get_boolean(value: str) -> bool:
    if value is True or (value == 'true' or value == 'True'):
        return True
    return False


def find_file(root_path, filename):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file == filename:
                log.info(f"!!! ---> Found {filename} at path {root}")
    log.info("Done searching for file")
