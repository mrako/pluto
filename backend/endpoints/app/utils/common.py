import logging as log
import json


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, e: Exception):
    log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def build_result_from_dict(result_dict: dict):
    result = {"success": True} | result_dict
    return result


def build_local_lambda_payload(data):
    return {"path": "/api",
            "httpMethod": "POST",
            "queryStringParameters": "",
            "headers": {
                "content-type": "application/json"
                },
            "body": json.dumps(data)}