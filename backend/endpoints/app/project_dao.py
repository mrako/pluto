import logging as log
from uuid import UUID

from api import db
from models import Project, ProjectOwner


def find_all_projects_by_org(organisation_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectOwner)\
        .filter(ProjectOwner.organisation_uuid == organisation_uuid)\
        .all()


def find_all_projects_by_user(user_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectOwner)\
        .filter(ProjectOwner.user_uuid == user_uuid)\
        .all()


def insert_project(project):
    log.info("Inserting a project not yet implemented")
