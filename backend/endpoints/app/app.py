import awsgi
from ariadne.constants import PLAYGROUND_HTML
from api import app, BASE_ROUTE
from ariadne import graphql_sync, ObjectType, load_schema_from_path, make_executable_schema, \
    snake_case_fallback_resolvers
from flask import request, jsonify
from services import project_service, repository_service
from services.flask_context_service import ContextBuilder, ContextCreationException
from utils.common import build_error_result
from utils.jwt_common import JWTParserInitialisationException

BASE_PATH = BASE_ROUTE + 'api'
ctx_builder = ContextBuilder()

query = ObjectType("Query")

query.set_field('projects', project_service.get_all_projects)
query.set_field('projectsByOrg', project_service.get_all_projects_by_org)
query.set_field('projectsByUser', project_service.get_all_projects_by_user)
query.set_field('project', project_service.get_project)
query.set_field('repository', repository_service.get_repository)

mutation = ObjectType("Mutation")
mutation.set_field('createProject', project_service.add_project_to_github)
mutation.set_field('updateDescription', project_service.update_project_data)
mutation.set_field('deleteProject', project_service.delete_project_from_github)
mutation.set_field('createRepository', repository_service.add_repository_to_github)
mutation.set_field('deleteRepository', repository_service.delete_repository_from_github)
mutation.set_field('bindPlutoUser', project_service.bind_user_to_installation)

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
    try:
        success, result = graphql_sync(
            schema,
            request.get_json(),
            context_value=ctx_builder.build_context(request),
            debug=app.debug
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code
    except ContextCreationException as e:
        return jsonify(build_error_result(
            "Bad Request", e,
            log_exception=False)), 400
    except JWTParserInitialisationException as e:
        return jsonify(build_error_result(
            "Internal server error", e)), 500


if __name__ == "__main__":
    ctx_builder = ContextBuilder(
        keys_file_path='../test_data/aws_keys.json',
        audience_claim=None,
        verify_token_expiration=False)
    app.run("0.0.0.0", port=8080, debug=True)
