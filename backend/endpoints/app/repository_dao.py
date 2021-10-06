import logging as log
from uuid import UUID, uuid4

from api import db
from models import Repository, ProjectRepository


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


def insert_repository(url: str, name: str, description: str):
    uuid = uuid4()
    db.session.add(Repository(uuid=uuid,
                              url=url,
                              name=name,
                              description=description))
    db.session.commit()
    return get_repository(uuid)
