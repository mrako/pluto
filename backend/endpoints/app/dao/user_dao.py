from uuid import uuid4

from api import db
from models import User


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
