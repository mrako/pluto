import requests
import logging as log
from flask import current_app as app
from uuid import UUID
from util import query_db, add_error, github_auth_headers, build_error_result

from ariadne import convert_kwargs_to_snake_case

from project_dao import find_all_projects_by_org, find_all_projects_by_user, find_project_by_org, find_project_by_user, \
    insert_project, find_all_projects, find_project, delete_project, update_project


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
    result = query_db('project', insert_project, name=name, description=description)
    resp = requests.post(app.config['GITHUB_BASE_URL']+"orgs/EficodeEntDemo/projects", headers=github_auth_headers(),
                         json={'name': name, 'body': description})
    if resp.status_code != 201:
        log.warning(f"Failed to create project with response code {resp.status_code}: {resp.text}")
        add_error(result, "Github project creation failed")
    return result


@convert_kwargs_to_snake_case
def update_project_data(*_, **request_fields):
    return query_db('project', update_project, **request_fields)


@convert_kwargs_to_snake_case
def delete_project_from_github(*_, project_uuid: UUID):
    return delete_from_db('project', delete_project, project_uuid=project_uuid)

