import logging as log
from uuid import UUID, uuid4

from api import db
from models import Repository, Project, ProjectRepository


def find_all_repositories():
    return db.session.query(Repository).all()


def find_repository(repository_uuid: UUID):
    return db.session.query(Repository)\
        .filter(Repository.uuid == repository_uuid)\
        .one_or_none()


def find_repository_by_url(repository_url: str):
    return db.session.query(Repository) \
        .filter(Repository.url == repository_url) \
        .one_or_none()


def get_repository(repository_uuid: UUID):
    return db.session.query(Repository)\
        .filter(Repository.uuid == repository_uuid).one()


def get_repositories_by_project_query(project: Project):
    return db.session.query(Repository)\
        .join(ProjectRepository, ProjectRepository.repository_uuid == Repository.uuid) \
        .filter(ProjectRepository.project_uuid == project.uuid)


def repository_exists(project: Project, repository_name: str):
    query = get_repositories_by_project_query(project) \
        .filter(Repository.name == repository_name)
    return db.session.query(query.exists()).scalar()


def insert_repository(url: str, name: str, description: str):
    uuid = uuid4()
    db.session.add(Repository(uuid=uuid,
                              url=url,
                              name=name,
                              description=description))
    db.session.flush()
    return get_repository(uuid)


def delete_repository(repository_uuid: UUID):
    repository = get_repository(repository_uuid)
    db.session.delete(repository)
    db.session.flush()
