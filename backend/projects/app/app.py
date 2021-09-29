import sys
import logging as log
import awsgi
from flask_cors import CORS
from flask import Flask, jsonify, request

import models
from project_dao import insert_project, get_all_projects
from project_service import add_project_to_github

root = log.getLogger()
root.setLevel(log.DEBUG)

handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

BASE_ROUTE = '/projects'
app = Flask(__name__)
CORS(app)


def handler(event, context):
    log.debug(f"received event: {event}")
    
    return awsgi.response(app, event, context)

    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         'Access-Control-Allow-Headers': '*',
    #         'Access-Control-Allow-Origin': '*',
    #         'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    #     },
    #     'body': json.dumps('Hello from your new Amplify Python lambda!')
    # }


@app.route(BASE_ROUTE, methods=['GET'])
def list_projects():
    return jsonify(get_all_projects())


@app.route(BASE_ROUTE, methods=['POST'])
def create_project():
    payload = request.get_json()
    log.debug(f"Payload: {payload}")
    insert_project(payload)
    add_project_to_github(payload)
    return jsonify(message="Project created")


if __name__ == "__main__":
    # execute only if run as a script
    app.run(debug=True)
