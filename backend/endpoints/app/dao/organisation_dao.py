from uuid import UUID, uuid4

from api import db
from models import Organisation, DataOrigin, UserLink, User, ProjectUser


def find_by_ext_id(data_origin: DataOrigin, ext_id):
    return db.session.query(Organisation)\
        .filter(Organisation.external_id == f"{ext_id}")\
        .filter(Organisation.data_origin_uuid == data_origin.uuid)\
        .one_or_none()


def get_by_installation_id(installation_id):
    return db.session.query(Organisation)\
        .filter(Organisation.installation_id == f"{installation_id}").one()


def create_org(data_origin: DataOrigin, installation_id: int, ext_id, name: str):
    uuid = uuid4()
    org = Organisation(
        uuid=uuid,
        data_origin_uuid=data_origin.uuid,
        external_id=f"{ext_id}",
        installation_id=installation_id,
        name=name
    )
    db.session.add(org)
    db.session.flush()
    return org


def find_by_user_account(user_account_uuid: UUID):
    return db.session.query(Organisation)\
        .join(UserLink, Organisation.uuid == UserLink.organisation_uuid)\
        .filter(UserLink.user_uuid == user_account_uuid)\
        .all()


def find_organisational_users(user_account_uuid: UUID):
    return db.session.query(ProjectUser)\
        .join(UserLink, ProjectUser.uuid == UserLink.project_user_uuid)\
        .filter(UserLink.user_uuid == user_account_uuid)\
        .filter(UserLink.organisation_uuid == None)\
        .all()
