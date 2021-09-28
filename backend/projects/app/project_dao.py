import logging as log
from models import Project


def get_all_projects():
    return [Project(id=1,
                    name="test-project",
                    description="foobar")]


def insert_project(project):
    log.info("Inserting a project not yet implemented")
