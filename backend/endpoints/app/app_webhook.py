import logging as log
import os

import awsgi
from flask import request

from api import app, BASE_ROUTE
import services.github_webhook_service as service

BASE_PATH = BASE_ROUTE + 'pluto-app'
WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET', None)
if not WEBHOOK_SECRET:
    log.error("GITHUB_WEBHOOK_SECRET environment variable not defined!")


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_PATH, methods=["POST"])
def receive_github_app_webhook():
    log.debug("Received Github App webhook call")
    if not app.debug:
        if not service.validate_github_request_sha256(
                request.headers.get('x-hub-signature-256', None),
                WEBHOOK_SECRET,
                request.data):
            log.error("Invalid webhook payload signature")
            return "Unauthorized", 401
        else:
            log.debug("Webhook signature verified")
    else:
        log.warning("Flask App Debug enabled !!! Not validating webhook secrets")

    payload = request.get_json()
    action = payload.get('action', None)
    try:
        log.debug(f"Executing action {action}")
        if action == "created":
            service.register_app_installation(payload)
        elif action == "suspend":
            service.deactivate_app_installation(payload)
        elif action == "unsuspend":
            service.activate_app_installation(payload)
        elif action == "deleted":
            service.remove_app_installation(payload)
        else:
            raise Exception(f"Unknown github app webhook action {action}")

        return "OK", 200
    except Exception as e:
        log.exception("Processing GitHub webhook action failed")
        return "Webhook processing failed", 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=8081, debug=True)
