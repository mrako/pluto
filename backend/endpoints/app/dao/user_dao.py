from uuid import uuid4, UUID

from api import db
from models import User, UserLink


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


def bind_users(pluto_user_id: UUID, project_user: UUID, organisation: UUID = None):
    uuid = uuid4()
    link = UserLink(uuid=uuid,
                    )