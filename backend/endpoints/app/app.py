import os
import logging as log
import awsgi
from ariadne.constants import PLAYGROUND_HTML
from api import app, BASE_ROUTE
from ariadne import graphql_sync, ObjectType, load_schema_from_path, make_executable_schema, \
    snake_case_fallback_resolvers
from flask import request, jsonify
from services import project_service, repository_service, user_service
from services.flask_context_service import ContextBuilder, ContextCreationException
from utils.common import build_error_result, get_boolean
from utils.jwt_common import JWTParserInitialisationException

BASE_PATH = BASE_ROUTE + 'api'
KEYS_FILE_PATH = os.environ.get('KEYS_FILE_PATH', None)
JWT_VALIDATE_EXPIRATION = get_boolean(os.environ.get('JWT_VALIDATE_EXPIRATION', True))
JWT_VALIDATE_AUDIENCE = get_boolean(os.environ.get('JWT_VALIDATE_AUDIENCE', True))
JWT_AUDIENCE_CLAIM = os.environ.get('JWT_AUDIENCE_CLAIM', 'sub')

if not JWT_VALIDATE_AUDIENCE:
    JWT_AUDIENCE_CLAIM = None

if KEYS_FILE_PATH is not None:
    log.warning(f"Using local file for public keys {KEYS_FILE_PATH}")

if not JWT_VALIDATE_EXPIRATION:
    log.warning("JWT expiration validation disabled!")

if not JWT_VALIDATE_AUDIENCE or JWT_AUDIENCE_CLAIM is None:
    log.warning("JWT audience validation disabled!")

ctx_builder = ContextBuilder(keys_file_path=KEYS_FILE_PATH,
                             verify_token_expiration=JWT_VALIDATE_EXPIRATION,
                             audience_claim=JWT_AUDIENCE_CLAIM)

query = ObjectType("Query")

query.set_field('projects', project_service.get_all_projects)
query.set_field('projectsByOrg', project_service.get_all_projects_by_org)
query.set_field('projectsByUser', project_service.get_all_projects_by_user)
query.set_field('project', project_service.get_project)
query.set_field('repository', repository_service.get_repository)
query.set_field('getOrganisationalInfo', user_service.get_user_organisational_info)

mutation = ObjectType("Mutation")
mutation.set_field('createProject', project_service.add_project)
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
        return jsonify(build_error_result("Bad Request")), 400
    except JWTParserInitialisationException as e:
        return jsonify(build_error_result("Internal server error")), 500


if __name__ == "__main__":
    ctx_builder = ContextBuilder(
        keys_file_path='../test_data/aws_keys.json',
        audience_claim=None,
        verify_token_expiration=False)
    app.run("0.0.0.0", port=8080, debug=True)
