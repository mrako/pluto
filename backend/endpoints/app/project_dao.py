import logging as log
from uuid import UUID, uuid4

from api import db
from models import Project, ProjectOwner, Repository


def find_all_projects():
    return db.session.query(Project).all()


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


def find_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid)\
        .one_or_none()


def find_project_by_org(organisation_uuid: UUID, project_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectOwner)\
        .filter(Project.uuid == project_uuid)\
        .filter(ProjectOwner.organisation_uuid == organisation_uuid)\
        .one_or_none()


def find_project_by_user(user_uuid: UUID, project_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectOwner)\
        .filter(Project.uuid == project_uuid)\
        .filter(ProjectOwner.user_uuid == user_uuid)\
        .one_or_none()


def get_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid).one()


def insert_project(name: str, description: str, repository: Repository = None, commit_transaction: bool = True):
    uuid = uuid4()
    project = Project(uuid=uuid,
                      name=name,
                      description=description)
    db.session.add(project)
    if repository:
        project.repositories.append(repository)
    if commit_transaction:
        db.session.commit()
    return get_project(uuid)


def update_project(project_uuid: UUID, **update_fields):
    db.session.query(Project).filter(Project.uuid == project_uuid).update(update_fields)
    db.session.commit()
    return get_project(project_uuid)


def delete_project(project_uuid: UUID):
    project = get_project(project_uuid)
    db.session.delete(project)
    db.session.commit()
