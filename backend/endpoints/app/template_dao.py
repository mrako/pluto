import logging as log
from uuid import UUID, uuid4

from api import db
from models import Template, ProjectRepository


def find_all_templates():
    return db.session.query(Template).all()

def find_template(template_name: str):
    return db.session.query(Template)\
        .filter(Template.template == template_name)\
        .one_or_none()

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


def insert_repository(url: str, name: str, description: str, commit_session: bool = True):
    uuid = uuid4()
    db.session.add(Repository(uuid=uuid,
                              url=url,
                              name=name,
                              description=description))
    if commit_session:
        db.session.commit()
    return get_repository(uuid)
