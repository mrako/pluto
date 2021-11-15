import logging as log
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from api import db
from utils.common import build_result, build_error_result, build_result_from_dict
from utils.db_common import query_db, update_db, delete_from_db

from ariadne import convert_kwargs_to_snake_case

import dao.project_dao as dao
import dao.user_dao as user_dao
from dao import project_dao, organisation_dao


@convert_kwargs_to_snake_case
def get_all_projects(obj, info):
    pluto_user_uuid = info.context['pluto_user'].uuid
    return query_db('projects', dao.find_all_projects, user_uuid=pluto_user_uuid)


@convert_kwargs_to_snake_case
def get_all_projects_by_org(obj, info, organisation_uuid: UUID):
    pluto_user_uuid = info.context['pluto_user'].uuid
    return query_db('projects',
                    dao.find_all_projects_by_org,
                    user_uuid=pluto_user_uuid,
                    organisation_uuid=organisation_uuid)


@convert_kwargs_to_snake_case
def get_project(obj, info, project_uuid: UUID):
    pluto_user_uuid = info.context['pluto_user'].uuid
    try:
        return query_db(
            'project',
            dao.get_project,
            user_uuid=pluto_user_uuid,
            project_uuid=project_uuid)
    except NoResultFound as e:
        return build_error_result("Bad Request", 400, e)


@convert_kwargs_to_snake_case
def add_project(obj, info, name: str, description: str, user_link_uuid: UUID):
    try:
        pluto_user_uuid = info.context['pluto_user'].uuid
        user_link = user_dao.get_user_link(pluto_user_uuid, user_link_uuid)
        if project_dao.project_exists(user_link, name):
            log.error(f"Project named {name} already exists for this user link")
            return build_error_result("Bad request", 400)

        proj = dao.insert_project(user_uuid=pluto_user_uuid,
                                  name=name,
                                  description=description)
        project_dao.insert_project_member(user_link, proj)
        db.session.commit()
        return build_result("project", proj)
    except NoResultFound as e:
        db.session.rollback()
        return build_error_result("Adding project failed", 400, e)
    except Exception as e:
        db.session.rollback()
        return build_error_result("Adding project failed", 500, e)


@convert_kwargs_to_snake_case
def update_project_data(obj, info, project_uuid: UUID, **update_fields):
    try:
        pluto_user_uuid = info.context['pluto_user'].uuid
        project_dao.get_project(user_uuid=pluto_user_uuid, project_uuid=project_uuid)
        result = update_db(
            'project',
            dao.update_project,
            user_uuid=pluto_user_uuid,
            project_uuid=project_uuid,
            **update_fields)
        db.session.commit()
        return result
    except NoResultFound as e:
        db.session.rollback()
        return build_error_result("Bad Request", 400, e)
    except Exception as e:
        db.session.rollback()
        return build_error_result("Updating project failed", 500, e)


@convert_kwargs_to_snake_case
def delete_project_from_github(obj, info, project_uuid: UUID):
    try:
        pluto_user_uuid = info.context['pluto_user'].uuid
        project_dao.get_project(user_uuid=pluto_user_uuid, project_uuid=project_uuid)
        result = delete_from_db(
            'project',
            dao.delete_project,
            user_uuid=pluto_user_uuid,
            project_uuid=project_uuid)
        db.session.commit()
        return result
    except NoResultFound as e:
        db.session.rollback()
        return build_error_result("Bad Request", 400, e)
    except Exception as e:
        db.session.rollback()
        return build_error_result("Deleting project failed", 500, e)


@convert_kwargs_to_snake_case
def bind_user_to_installation(obj, info, installation_id: str, code: str):
    try:
        user = info.context['pluto_user']
        user_uuid = user.uuid
        project_user = project_dao.get_user_by_installation_id(installation_id)
        org = organisation_dao.get_by_installation_id(installation_id)
        user_dao.bind_users(pluto_user_uuid=user_uuid,
                            project_user_uuid=project_user.uuid,
                            code=code,
                            organisation_uuid=org.uuid)
        db.session.commit()
        return build_result_from_dict({'user_account': user,
                                       'project_user': project_user,
                                       'organisation': org}, status_code=201)
    except NoResultFound as e:
        db.session.rollback()
        return build_error_result("Bad Request", 400, e)
    except IntegrityError as e:
        return build_error_result(f"Bad request", 400, e)
    except Exception as e:
        return build_error_result(
            f"Binding pluto user {user_uuid} to installation {installation_id} failed", 500,
            e)
