import os
from uuid import uuid4
import logging as log


def get_all_projects():
    return {'name': 'test-project'}


def insert_project(project):
    log.info("Inserting a project not yet implemented")
