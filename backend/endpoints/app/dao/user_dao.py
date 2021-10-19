from uuid import uuid4, UUID

from api import db
from models import User, UserLink


def get_user(user_uuid: UUID):
    return db.session.query(User)\
        .filter(User.uuid == user_uuid).one()


def create_user(username: str, email: str, name: str):
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


def bind_users(pluto_user_uuid: UUID, project_user_uuid: UUID, organisation_uuid: UUID = None):
    uuid = uuid4()
    link = UserLink(uuid=uuid,
                    user_uuid=pluto_user_uuid,
                    project_user_uuid=project_user_uuid,
                    organisation_uuid=organisation_uuid)
    db.session.add(link)
    db.session.commit()
    return link
