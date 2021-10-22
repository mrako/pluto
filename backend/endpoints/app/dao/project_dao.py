from uuid import UUID, uuid4

from api import db
from models import Project, Repository, ProjectMember, DataOrigin, ProjectUser, UserLink


def find_all_projects():
    return db.session.query(Project).all()


def find_all_projects_by_org(organisation_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember)\
        .join(UserLink)\
        .filter(UserLink.organisation_uuid == organisation_uuid)\
        .all()


def find_all_projects_by_user(user_uuid: UUID):
    return db.session.query(Project)\
        .join(ProjectMember) \
        .join(UserLink) \
        .filter(UserLink.user_uuid == user_uuid)\
        .all()


def find_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid)\
        .one_or_none()


def get_project(project_uuid: UUID):
    return db.session.query(Project)\
        .filter(Project.uuid == project_uuid).one()


def insert_project(name: str, description: str, repository: Repository = None, commit_transaction: bool = True):
    uuid = uuid4()
    project = Project(uuid=uuid,
                      name=name,
                      description=description)
    db.session.add(project)
    if repository:
        project.repositories.append(repository)
    if commit_transaction:
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


def find_user_by_ext_id(data_origin: DataOrigin, ext_id):
    return db.session.query(ProjectUser)\
        .filter(ProjectUser.external_id == f"{ext_id}")\
        .filter(ProjectUser.data_origin_uuid == data_origin.uuid)\
        .one_or_none()


def get_user_by_installation_id(installation_id):
    return db.session.query(ProjectUser)\
        .filter(ProjectUser.installation_id == f"{installation_id}").one()


def create_project_user(data_origin: DataOrigin, installation_id: int, ext_id, username: str):
    uuid = uuid4()
    user = ProjectUser(
        uuid=uuid,
        data_origin_uuid=data_origin.uuid,
        external_id=f"{ext_id}",
        installation_id=installation_id,
        username=username
    )
    db.session.add(user)
    db.session.commit()
    return user
