import logging as log

from api import app
from flask import request
from services import cognito_service
from services.cognito_service import InvalidUserException

BASE_ROUTE = '/post-confirm'


def handler(event, context):
    receive_aws_post_confirmation_hook(event)
    return event


def receive_aws_post_confirmation_hook(event):
    try:
        user_attributes = event.get('request', {}).get('userAttributes', {})
        if not user_attributes.get('email_verified', False):
            log.error("Invalid post confirmation. Email was not verified.")
        else:
            cognito_service.create_user(user_attributes)
    except InvalidUserException:
        log.exception("Received invalid user payload")
        raise Exception("Post confirmation hook failed")
    except Exception as e:
        log.exception("Processing Cognito post confirmation failed")
        raise Exception("Post confirmation hook failed")


@app.route(BASE_ROUTE, methods=["POST"])
def test_endpoint():
    payload = request.get_json()
    log.info(f"PAYLOAD {payload}")
    receive_aws_post_confirmation_hook(payload)

    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8083, debug=True)
