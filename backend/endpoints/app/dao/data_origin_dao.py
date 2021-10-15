from api import db
from models import Organisation, DataOrigin


def get_data_origin_by_name(name: str):
    return db.session.query(DataOrigin).filter(DataOrigin.name == name).one()
