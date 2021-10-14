import logging as log
import os

import awsgi
from flask import request

from api import app

BASE_ROUTE = '/pluto-post-confirm'


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_ROUTE, methods=["POST"])
def receive_aws_post_confirmation_hook():

    payload = request.get_json()
    try:

        return "OK", 200
    except Exception as e:
        log.exception("Processing GitHub webhook action failed")
        return "Webhook processing failed", 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=8083, debug=True)
