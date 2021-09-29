import logging as log

from project_dao import find_all_projects


def get_all_projects(obj, info):
    try:
        projects = find_all_projects()
        return {"success": True,
                "projects": projects}
    except:
        msg = 'Retrieving projects failed'
        log.exception(msg)
        return {
            "success": False,
            "errors": [msg]
        }


def add_project_to_github(project):
    pass
