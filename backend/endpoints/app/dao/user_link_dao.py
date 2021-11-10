from uuid import UUID

from api import db
from models import UserLink


def find_user_links(user_account_uuid: UUID):
    return db.session.query(UserLink)\
        .filter(UserLink.user_uuid == user_account_uuid)\
        .all()


def find_organisation_links(org_uuid: UUID):
    return db.session.query(UserLink)\
        .filter(UserLink.organisation_uuid == org_uuid)\
        .all()


def delete_user_links(user_account_uuid: UUID):
    db.session.query(UserLink)\
        .filter(UserLink.user_uuid == user_account_uuid)\
        .delete()


def delete_organisation_links(org_uuid: UUID):
    db.session.query(UserLink)\
        .filter(UserLink.organisation_uuid == org_uuid)\
        .delete()
