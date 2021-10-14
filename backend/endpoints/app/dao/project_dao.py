from uuid import UUID, uuid4

from api import db
from models import Project, ProjectMember, DataOrigin, ProjectUser


def find_all_projects():
    return db.session.query(Project).all()


def find_all_projects_by_org(organisation_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember)\
        .filter(ProjectMember.organisation_uuid == organisation_uuid)\
        .all()


def find_all_projects_by_user(user_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember)\
        .filter(ProjectMember.user_uuid == user_uuid)\
        .all()


def find_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid)\
        .one_or_none()


def find_project_by_org(organisation_uuid: UUID, project_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember)\
        .filter(Project.uuid == project_uuid)\
        .filter(ProjectMember.organisation_uuid == organisation_uuid)\
        .one_or_none()


def find_project_by_user(user_uuid: UUID, project_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember)\
        .filter(Project.uuid == project_uuid)\
        .filter(ProjectMember.user_uuid == user_uuid)\
        .one_or_none()


def get_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid).one()


def insert_project(name: str, description: str):
    uuid = uuid4()
    db.session.add(Project(uuid=uuid,
                           name=name,
                           description=description))
    db.session.commit()
    return get_project(uuid)


def update_project(project_uuid: UUID, **update_fields):
    db.session.query(Project).filter(Project.uuid == project_uuid).update(update_fields)
    db.session.commit()
    return get_project(project_uuid)


def delete_project(project_uuid: UUID):
    project = get_project(project_uuid)
    db.session.delete(project)
    db.session.commit()


def find_user_by_ext_id(data_origin: DataOrigin, ext_id: str):
    return db.session.query(ProjectUser)\
        .filter(ProjectUser.external_id == ext_id)\
        .filter(ProjectUser.data_origin_uuid == data_origin.uuid)\
        .one_or_none()


def create_project_user(data_origin: DataOrigin, ext_id: str, username: str):
    uuid = uuid4()
    user = ProjectUser(
        uuid=uuid,
        data_origin_uuid=data_origin.uuid,
        external_id=ext_id,
        username=username
    )
    db.session.add(user)
    db.session.commit()
    return user
