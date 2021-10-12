import logging as log
import os

import awsgi
from flask import request

from api import app
from services.github_webhook_service import validate_github_request_sha256

BASE_ROUTE = '/pluto-app'
WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET', None)
if not WEBHOOK_SECRET:
    log.error("GITHUB_WEBHOOK_SECRET environment variable not defined!")


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_ROUTE, methods=["POST"])
def receive_github_app_webhook():
    if not validate_github_request_sha256(
            request.headers.get('x-hub-signature-256', None),
            WEBHOOK_SECRET,
            request.data):
        return "Unauthorized", 401

    payload = request.get_json()
    log.info(f"Received payload {payload}")
    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8081, debug=True)
