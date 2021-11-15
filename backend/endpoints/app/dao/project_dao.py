from uuid import UUID, uuid4

from api import db
from models import Project, Repository, ProjectMember, DataOrigin, ProjectUser, UserLink, ProjectUserAttribute


def find_projects_query():
    return db.session.query(Project) \
        .join(ProjectMember, ProjectMember.project_uuid == Project.uuid) \
        .join(UserLink, UserLink.uuid == ProjectMember.user_link_uuid)


def find_all_projects(user_uuid: UUID):
    return find_projects_query()\
        .filter(UserLink.user_uuid == user_uuid)\
        .all()


def find_all_projects_by_org(user_uuid: UUID, organisation_uuid: UUID):
    return find_projects_query() \
        .filter(UserLink.user_uuid == user_uuid) \
        .filter(UserLink.organisation_uuid == organisation_uuid)\
        .all()


def get_project_query(user_uuid: UUID, project_uuid: UUID):
    return find_projects_query() \
        .filter(UserLink.user_uuid == user_uuid) \
        .filter(Project.uuid == project_uuid)


def get_project(user_uuid: UUID, project_uuid: UUID):
    return get_project_query(user_uuid, project_uuid).one()


def get_projects_by_user_link_query(user_link: UserLink):
    return db.session.query(Project)\
        .join(ProjectMember, ProjectMember.project_uuid == Project.uuid) \
        .filter(ProjectMember.user_link_uuid == user_link.uuid)


def project_exists(user_link: UserLink, name: str):
    query = get_projects_by_user_link_query(user_link) \
        .filter(Project.name == name)
    return db.session.query(query.exists()).scalar()


def insert_project(name: str, description: str, repository: Repository = None):
    uuid = uuid4()
    project = Project(uuid=uuid,
                      name=name,
                      description=description)
    db.session.add(project)
    if repository:
        project.repositories.append(repository)
    db.session.flush()
    return get_project(uuid)


def insert_project_member(user_link: UserLink, project: Project):
    project_member = ProjectMember(user_link_uuid=user_link.uuid, project_uuid=project.uuid)
    db.session.add(project_member)
    db.session.flush()
    return project_member


def update_project(project_uuid: UUID, **update_fields):
    db.session.query(Project).filter(Project.uuid == project_uuid).update(update_fields)
    db.session.flush()
    return get_project(project_uuid)


def delete_project(project_uuid: UUID):
    project = get_project(project_uuid)
    db.session.delete(project)
    db.session.flush()


def find_user_by_ext_id(data_origin: DataOrigin, ext_id):
    return db.session.query(ProjectUser)\
        .filter(ProjectUser.external_id == f"{ext_id}")\
        .filter(ProjectUser.data_origin_uuid == data_origin.uuid)\
        .one_or_none()


def get_user_by_installation_id(installation_id):
    return db.session.query(ProjectUser)\
        .join(ProjectUserAttribute, ProjectUserAttribute.project_user_uuid == ProjectUser.uuid) \
        .filter(ProjectUserAttribute.name == 'installation_id') \
        .filter(ProjectUserAttribute.value == f"{installation_id}")\
        .one()


def create_project_user(data_origin: DataOrigin, ext_id, username: str):
    uuid = uuid4()
    user = ProjectUser(
        uuid=uuid,
        data_origin_uuid=data_origin.uuid,
        external_id=f"{ext_id}",
        username=username
    )
    db.session.add(user)
    db.session.flush()
    return user


def add_installation_id(user: ProjectUser, installation_id: int):
    attribute = ProjectUserAttribute(
        uuid=uuid4(),
        project_user_uuid=user.uuid,
        name='installation_id',
        value=installation_id
    )
    db.session.add(attribute)
    db.session.flush()
