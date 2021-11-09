from uuid import UUID

import dao.user_dao as dao
from api import db


class InvalidUserException(Exception):
    pass


def create_user(username: str, user_attributes):
    uuid = UUID(user_attributes.get('sub', None))
    existing_user = dao.find_user(uuid)
    if existing_user is not None:
        return existing_user

    email = user_attributes.get('email', None)
    name = user_attributes.get('name', None)

    if username and email:
        user = dao.create_user(uuid, username, email, name)
        db.session.commit()
        return user
    else:
        raise InvalidUserException("Username or email not defined")
