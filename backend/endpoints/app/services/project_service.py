import requests
import logging as log
from flask import current_app as app
from uuid import UUID
from api import db
from util import query_db, github_auth_headers, build_result, build_error_result

from ariadne import convert_kwargs_to_snake_case

import dao.project_dao as dao
import dao.user_dao as user_dao
from dao import project_dao, organisation_dao


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_result_from_dict(result_dict: dict):
    result = {"success": True} | result_dict
    return result


def build_error_result(message: str, e: Exception):
    log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def query_db(result_field_name: str, dao_function, **kwargs):
    return execute_db(result_field_name, dao_function, operation='Retrieving', **kwargs)


def update_db(result_field_name: str, dao_function, **kwargs):
    return execute_db(result_field_name, dao_function, operation='Updating', **kwargs)


def execute_db(result_field_name: str, dao_function, operation: str = 'Querying', **kwargs):
    try:
        # Execute the dao method and return result
        return build_result(result_field_name, dao_function(**kwargs))
    except Exception as e:
        msg = f"{operation} {result_field_name} failed"
        return build_error_result(msg, e)


def delete_from_db(object_name: str, dao_function, **kwargs):
    try:
        # Execute the dao method
        dao_function(**kwargs)

        # Return result
        return {"success": True}
    except Exception as e:
        msg = f"Deleting {object_name} with args {kwargs} failed"
        return build_error_result(msg, e)


@convert_kwargs_to_snake_case
def get_all_projects(*_):
    return query_db('projects', dao.find_all_projects)


@convert_kwargs_to_snake_case
def get_all_projects_by_org(*_, organisation_uuid: UUID):
    return query_db('projects', dao.find_all_projects_by_org, organisation_uuid=organisation_uuid)


@convert_kwargs_to_snake_case
def get_all_projects_by_user(*_, user_uuid: UUID):
    return query_db('projects', dao.find_all_projects_by_user, user_uuid=user_uuid)


@convert_kwargs_to_snake_case
def get_project(*_, project_uuid: UUID):
    return query_db('project', dao.find_project, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def get_project_by_org(*_, organisation_uuid: UUID, project_uuid: UUID):
    return query_db('project', dao.find_project_by_org, organisation_uuid=organisation_uuid, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def get_project_by_user(*_, user_uuid: UUID, project_uuid: UUID):
    return query_db('project', dao.find_project_by_user, user_uuid=user_uuid, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def add_project_to_github(*_, name: str, description: str):
    try:
        proj = dao.insert_project(name=name,
                                  description=description,
                                  commit_transaction=False)
        resp = requests.post(f"{app.config['GITHUB_BASE_URL']}orgs/{app.config['GITHUB_ORG_NAME']}/projects",
                             headers=github_auth_headers(),
                             json={'name': name, 'body': description})
        if resp.status_code != 201:
            raise Exception(f"Failed to create project with response code {resp.status_code}: {resp.text}")
        return build_result("project", proj)
    except Exception as e:
        db.session.rollback()
        return build_error_result(str(e), e)


@convert_kwargs_to_snake_case
def update_project_data(*_, **request_fields):
    return update_db('project', dao.update_project, **request_fields)


@convert_kwargs_to_snake_case
def delete_project_from_github(*_, project_uuid: UUID):
    return delete_from_db('project', dao.delete_project, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def bind_user_to_installation(*_, installation_id: str, pluto_user_uuid: UUID):
    try:
        user = user_dao.get_user(pluto_user_uuid)
        project_user = project_dao.get_user_by_installation_id(installation_id)
        org = organisation_dao.get_by_installation_id(installation_id)
        user_dao.bind_users(pluto_user_uuid=user.uuid,
                            project_user_uuid=project_user.uuid,
                            organisation_uuid=org.uuid)
        return build_result_from_dict({'user_account': user,
                                       'project_user': project_user,
                                       'organisation': org})
    except Exception as e:
        msg = f"Binding pluto user {pluto_user_uuid} to installation {installation_id} failed"
        return build_error_result(msg, e)

