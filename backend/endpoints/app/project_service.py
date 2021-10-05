import logging as log
from uuid import UUID
from ariadne import convert_kwargs_to_snake_case

from project_dao import find_all_projects_by_org, find_all_projects_by_user, find_project_by_org, find_project_by_user, \
    insert_project, find_all_projects, find_project


def query_db(*args, **kwargs):
    field_name = args[0]
    try:
        return {"success": True,
                field_name: args[1](**kwargs)}
    except:
        msg = f"Retrieving {field_name} failed"
        log.exception(msg)
        return {
            "success": False,
            "errors": [msg]
        }


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


def add_project_to_github(*_, name: str, description: str):
    result = query_db('project', insert_project, name=name, description=description)
    return result

