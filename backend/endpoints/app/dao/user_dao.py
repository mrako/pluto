from uuid import uuid4, UUID

from api import db
from models import User, UserLink


def get_user(user_uuid: UUID):
    return db.session.query(User)\
        .filter(User.uuid == user_uuid).one()


def create_user(uuid: UUID, username: str, email: str, name: str):
    if not uuid:
        uuid = uuid4()
    user = User(
        uuid=uuid,
        username=username,
        email=email,
        name=name
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_link_for_by_user_uuid(user_uuid: UUID):
    return db.session.query(UserLink) \
        .filter(UserLink.user_uuid == user_uuid).one()


def bind_users(pluto_user_uuid: UUID, project_user_uuid: UUID, code: str, organisation_uuid: UUID = None):
    uuid = uuid4()
    link = UserLink(uuid=uuid,
                    user_uuid=pluto_user_uuid,
                    project_user_uuid=project_user_uuid,
                    organisation_uuid=organisation_uuid,
                    code=code)
    db.session.add(link)
    db.session.commit()
    return link
