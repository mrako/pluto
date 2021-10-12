import logging as log
from uuid import UUID
from ariadne import convert_kwargs_to_snake_case

from dao.project_dao import find_all_projects, find_all_projects_by_org, find_all_projects_by_user, find_project, \
    find_project_by_org, find_project_by_user, insert_project, update_project, delete_project


def build_result(result_field_name: str, result):
    return {"success": True, result_field_name: result}


def build_error_result(message: str, e: Exception):
    log.error(message, exc_info=e)
    return {"success": False, "errors": [message]}


def query_db(result_field_name: str, dao_function, **kwargs):
    try:
        # Execute the dao method and return result
        return build_result(result_field_name, dao_function(**kwargs))
    except Exception as e:
        msg = f"Retrieving {result_field_name} failed"
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
    return query_db('projects', find_all_projects)


@convert_kwargs_to_snake_case
def get_all_projects_by_org(*_, organisation_uuid: UUID):
    return query_db('projects', find_all_projects_by_org, organisation_uuid=organisation_uuid)


@convert_kwargs_to_snake_case
def get_all_projects_by_user(*_, user_uuid: UUID):
    return query_db('projects', find_all_projects_by_user, user_uuid=user_uuid)


@convert_kwargs_to_snake_case
def get_project(*_, project_uuid: UUID):
    return query_db('project', find_project, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def get_project_by_org(*_, organisation_uuid: UUID, project_uuid: UUID):
    return query_db('project', find_project_by_org, organisation_uuid=organisation_uuid, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def get_project_by_user(*_, user_uuid: UUID, project_uuid: UUID):
    return query_db('project', find_project_by_user, user_uuid=user_uuid, project_uuid=project_uuid)


@convert_kwargs_to_snake_case
def add_project_to_github(*_, name: str, description: str):
    return query_db('project', insert_project, name=name, description=description)


@convert_kwargs_to_snake_case
def update_project_data(*_, **request_fields):
    return query_db('project', update_project, **request_fields)


@convert_kwargs_to_snake_case
def delete_project_from_github(*_, project_uuid: UUID):
    return delete_from_db('project', delete_project, project_uuid=project_uuid)

