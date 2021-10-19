import awsgi
from ariadne.constants import PLAYGROUND_HTML

from api import app, BASE_ROUTE
from ariadne import graphql_sync, ObjectType, load_schema_from_path, make_executable_schema, \
    snake_case_fallback_resolvers
from flask import request, jsonify

import services.project_service as project_service

BASE_PATH = BASE_ROUTE + 'api'

query = ObjectType("Query")
query.set_field('projects', project_service.get_all_projects)
query.set_field('projectsByOrg', project_service.get_all_projects_by_org)
query.set_field('projectsByUser', project_service.get_all_projects_by_user)
query.set_field('project', project_service.get_project)
query.set_field('projectByOrg', project_service.get_project_by_org)
query.set_field('projectByUser', project_service.get_project_by_user)

mutation = ObjectType("Mutation")
mutation.set_field('createProject', project_service.add_project_to_github)
mutation.set_field('updateDescription', project_service.update_project_data)
mutation.set_field('deleteProject', project_service.delete_project_from_github)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


def handler(event, context):
    return awsgi.response(app, event, context)


@app.route(BASE_PATH, methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route(BASE_PATH, methods=["POST"])
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
