import logging as log
from models import Project


def find_all_projects():
    return [Project(id=1,
                    name="test-project",
                    description="foobar"),
            Project(id=2,
                    name="test-project-2",
                    description="foobarfoo")
            ]


def insert_project(project):
    log.info("Inserting a project not yet implemented")
