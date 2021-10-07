import awsgi
from ariadne.constants import PLAYGROUND_HTML

from api import app
from ariadne import graphql_sync, ObjectType, load_schema_from_path, make_executable_schema, \
    snake_case_fallback_resolvers
from flask import request, jsonify

from project_service import get_all_projects_by_org, get_all_projects_by_user, add_project_to_github, \
    get_all_projects, get_project, delete_project_from_github, update_project_data

from repository_service import get_repository, add_repository_to_github, delete_repository_from_github

BASE_ROUTE = '/api'

query = ObjectType("Query")
query.set_field('projects', get_all_projects)
query.set_field('projectsByOrg', get_all_projects_by_org)
query.set_field('projectsByUser', get_all_projects_by_user)
query.set_field('project', get_project)
query.set_field('projectByOrg', get_all_projects_by_user)
query.set_field('projectByUser', get_all_projects_by_user)
query.set_field('repository', get_repository)

mutation = ObjectType("Mutation")
mutation.set_field('createProject', add_project_to_github)
mutation.set_field('createRepository', add_repository_to_github)
mutation.set_field('updateDescription', update_project_data)
mutation.set_field('deleteProject', delete_project_from_github)
mutation.set_field('deleteRepository', delete_repository_from_github)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
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
