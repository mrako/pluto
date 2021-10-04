import logging as log
from uuid import UUID
from ariadne import convert_kwargs_to_snake_case

from project_dao import find_all_projects_by_org, find_all_projects_by_user


def foo(*args, **kwargs):
    print(f"{args}")
    print(f"{kwargs}")
    print(f"? : {kwargs.get('foo', None)} {kwargs.get('bar', None)}")


def query_db(*args, **kwargs):
    field_name = args[0]
    try:
        return {"success": True,
                field_name: args[1](kwargs)}
    except:
        msg = f"Retrieving {field_name} failed"
        log.exception(msg)
        return {
            "success": False,
            "errors": [msg]
        }


@convert_kwargs_to_snake_case
def get_all_projects_by_org(*_, organisation_uuid=None):
    log.debug(f"RUNNING QUERY!!!")
    result = query_db('projectsByOrg', find_all_projects_by_org, organisation_uuid=organisation_uuid)
    log.debug(f"Result: {result}")
    return result


@convert_kwargs_to_snake_case
def get_all_projects_by_user(*_, user_uuid: UUID):
    return query_db('projectsByUser', find_all_projects_by_user, user_uuid=user_uuid)


def add_project_to_github(project):
    pass
