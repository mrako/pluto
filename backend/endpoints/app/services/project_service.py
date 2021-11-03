import logging as log
import requests
from flask import current_app as app
from uuid import UUID
from api import db
from utils.common import build_result, build_error_result, build_result_from_dict
from utils.db_common import query_db, update_db, delete_from_db
from utils.github_common import github_auth_headers

from ariadne import convert_kwargs_to_snake_case

import dao.project_dao as dao
import dao.user_dao as user_dao
from dao import project_dao, organisation_dao


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
def add_project(obj, info, name: str, description: str, user_link_uuid: UUID):
    try:
        user_link = user_dao.get_user_link_by_uuid(user_link_uuid)
        proj = dao.insert_project(name=name,
                                  description=description,
                                  commit_transaction=False)
        project_dao.insert_project_member(user_link, proj)
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
def bind_user_to_installation(*_, installation_id: str, code: str, pluto_user_uuid: UUID):
    try:
        user = user_dao.get_user(pluto_user_uuid)
        project_user = project_dao.get_user_by_installation_id(installation_id)
        org = organisation_dao.get_by_installation_id(installation_id)
        user_dao.bind_users(pluto_user_uuid=user.uuid,
                            project_user_uuid=project_user.uuid,
                            code=code,
                            organisation_uuid=org.uuid)
        return build_result_from_dict({'user_account': user,
                                       'project_user': project_user,
                                       'organisation': org})
    except Exception as e:
        msg = f"Binding pluto user {pluto_user_uuid} to installation {installation_id} failed"
        return build_error_result(msg, e)

