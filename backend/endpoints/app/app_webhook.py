import awsgi

from api import app

BASE_ROUTE = '/pluto-app'


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_ROUTE, methods=["POST"])
def receive_github_app_webhook():
    return "OK", 200
