import sys
import logging as log
import awsgi
from api import app, db
from flask_sqlalchemy import SQLAlchemy
from project_dao import get_all_projects
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

root = log.getLogger()
root.setLevel(log.DEBUG)

handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

BASE_ROUTE = '/projects'
query = ObjectType("Query")
query.set_field("projects", get_all_projects())
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)


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


@app.route(BASE_ROUTE, methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route(BASE_ROUTE, methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
