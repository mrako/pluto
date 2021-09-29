import logging as log
from models import Project


def get_all_projects(obj, info):
    projects = [Project(id=1,
                    name="test-project",
                    description="foobar")]
    return {"success": True,
            "projects": projects}


def insert_project(project):
    log.info("Inserting a project not yet implemented")
