import logging as log
from api import app, BASE_ROUTE
from flask import request
import services.template_service as service
from utils.common import build_error_result, success_result

BASE_PATH = BASE_ROUTE + 'pluto-git'


def handler(event, context):
    handle_template_service_call(event)
    return event


def handle_template_service_call(event):
    try:
        service.push_repository_template(event.get('user_uuid'),
                                         event.get('repo_url'),
                                         event.get('template'),
                                         event.get('github_auth_token'),
                                         event.get('branch', None))
    except Exception as e:
        return build_error_result("Pushing repository template failed", e)
    return success_result


@app.route(BASE_PATH, methods=["POST"])
def test_endpoint():
    payload = request.get_json()
    log.info(f"PAYLOAD {payload}")
    handle_template_service_call(payload)

    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8085, debug=True)
