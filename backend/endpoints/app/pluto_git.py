import logging as log
from requests import request
from api import app, BASE_ROUTE
import services.template_service as service

BASE_PATH = BASE_ROUTE + 'pluto-git'


def handler(event, context):
    handle_template_service_call(event)
    return event


def handle_template_service_call(event):
    service.run_template_service(event.get('user_uuid'),
                                 event.get('repo_url'),
                                 event.get('template'),
                                 event.get('github_auth_token'),
                                 event.get('branch', None))


@app.route(BASE_PATH, methods=["POST"])
def test_endpoint():
    payload = request.get_json()
    log.info(f"PAYLOAD {payload}")
    handle_template_service_call(payload)

    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8085, debug=True)
