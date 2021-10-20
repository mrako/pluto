import logging as log
from api import app, db
from flask import request

BASE_ROUTE = '/db_setup'


def handler(event, context):
    setup_db(event)
    return event


def setup_db(event):
    pass


@app.route(BASE_ROUTE, methods=["POST"])
def test_endpoint():
    payload = request.get_json()
    log.info(f"PAYLOAD {payload}")
    setup_db(payload)

    return "OK", 200


if __name__ == "__main__":
    app.run("0.0.0.0", port=8084, debug=True)
