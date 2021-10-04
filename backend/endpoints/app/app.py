import awsgi
from ariadne.constants import PLAYGROUND_HTML

from api import app
from ariadne import graphql_sync, ObjectType, load_schema_from_path, make_executable_schema, \
    snake_case_fallback_resolvers
from flask import request, jsonify

from project_service import get_all_projects_by_org

BASE_ROUTE = '/api'

query = ObjectType("Query")
query.set_field('projectsByOrg', get_all_projects_by_org)
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_ROUTE, methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


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


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)
