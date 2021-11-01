import logging as log

from api import app, BASE_ROUTE
from flask import request
from services import cognito_service
from services.cognito_service import InvalidUserException

BASE_PATH = BASE_ROUTE + 'post-confirm'


def handler(event, context):
    receive_aws_post_confirmation_hook(event)
    return event


def receive_aws_post_confirmation_hook(event):
    log.debug(f"Event: {event}")
    try:
        username = event.get('username', None)
        if not username:
            raise Exception("Invalid post confirmation. Username was not defined")

        user_attributes = event.get('request', {}).get('userAttributes', {})
        if not user_attributes.get('email_verified', False):
            raise Exception("Invalid post confirmation. Email was not verified.")

        cognito_service.create_user(username, user_attributes)
    except InvalidUserException:
        log.exception("Received invalid user payload")
        raise Exception("Post confirmation hook failed")
    except Exception as e:
        log.exception("Processing Cognito post confirmation failed")
        raise Exception("Post confirmation hook failed")


@app.route(BASE_PATH, methods=["POST"])
def test_endpoint():
    payload = request.get_json()
    log.info(f"PAYLOAD {payload}")
    receive_aws_post_confirmation_hook(payload)

    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8083, debug=True)
