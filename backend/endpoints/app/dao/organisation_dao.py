from uuid import UUID, uuid4

from api import db
from models import Organisation, DataOrigin


def find_by_ext_id(data_origin: DataOrigin, ext_id: str):
    return db.session.query(Organisation)\
        .filter(Organisation.external_id == ext_id)\
        .filter(Organisation.data_origin_uuid == data_origin.uuid)\
        .one_or_none()


def create_org(data_origin: DataOrigin, ext_id: str, name: str):
    uuid = uuid4()
    org = Organisation(
        uuid=uuid,
        data_origin_uuid=data_origin.uuid,
        external_id=ext_id,
        name=name
    )
    db.session.add(org)
    db.session.commit()
    return org
