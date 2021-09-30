import sys
import logging as log
import awsgi
from api import app, db
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from flask import request, jsonify

from project_service import get_all_projects

root = log.getLogger()
root.setLevel(log.DEBUG)

handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

BASE_ROUTE = '/projects'
query = ObjectType("Query")
query.set_field("projects", get_all_projects)
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_ROUTE, methods=["POST"])
def graphql_server():
    success, result = graphql_sync(
        schema,
        request.get_json(),
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
