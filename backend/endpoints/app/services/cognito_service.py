import dao.user_dao as dao
from api import db


class InvalidUserException(Exception):
    pass


def create_user(username: str, user_attributes):
    uuid = user_attributes.get('sub', None)
    email = user_attributes.get('email', None)
    name = user_attributes.get('name', None)

    if username and email:
        user = dao.create_user(uuid, username, email, name)
        db.session.commit()
        return user
    else:
        raise InvalidUserException("Username or email not defined")
