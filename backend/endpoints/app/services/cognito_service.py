import dao.user_dao as dao


class InvalidUserException(Exception):
    pass


def create_user(user_attributes):
    username = user_attributes.get('username', None)
    email = user_attributes.get('email', None)
    name = user_attributes.get('name', None)

    if username and email:
        return dao.create_user(username, email, name)
    else:
        raise InvalidUserException("Username or email not defined")
