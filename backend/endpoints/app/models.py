from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint

Base = declarative_base()


class DataOrigin(Base):
    __tablename__ = "data_origin"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "user_account"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)


class ProjectUser(Base):
    __tablename__ = "project_user"
    __table_args__ = (
        UniqueConstraint('data_origin_uuid', 'external_id'),
        UniqueConstraint('data_origin_uuid', 'username')
    )
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_origin_uuid = Column(UUID(as_uuid=True), ForeignKey('data_origin.uuid'), nullable=False)
    external_id = Column(String, nullable=False)
    installation_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String)


class Organisation(Base):
    __tablename__ = "organisation"
    __table_args__ = (
        UniqueConstraint('data_origin_uuid', 'external_id'),
        UniqueConstraint('data_origin_uuid', 'name')
    )
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_origin_uuid = Column(UUID(as_uuid=True), ForeignKey('data_origin.uuid'), nullable=False)
    external_id = Column(String, nullable=False)
    installation_id = Column(String, nullable=False)
    name = Column(String, nullable=False)


class ProjectBoard(Base):
    __tablename__ = "project_board"
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), primary_key=True, onupdate="CASCADE")
    board_uuid = Column(UUID(as_uuid=True), ForeignKey('board.uuid'), primary_key=True, onupdate="CASCADE")


class ProjectRepository(Base):
    __tablename__ = "project_repository"
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), primary_key=True, onupdate="CASCADE")
    repository_uuid = Column(UUID(as_uuid=True), ForeignKey('repository.uuid'), primary_key=True, onupdate="CASCADE")


class Project(Base):
    __tablename__ = "project"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    boards = relationship(
        'Board',
        secondary='project_board',
        back_populates="projects",
        cascade="save-update"
    )
    repositories = relationship(
        'Repository',
        secondary='project_repository',
        back_populates="projects",
        cascade="save-update"
    )


class Repository(Base):
    __tablename__ = "repository"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    projects = relationship(
        'Project',
        secondary='project_repository'
    )


class Board(Base):
    __tablename__ = "board"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    projects = relationship(
        'Project',
        secondary='project_board'
    )


class UserLink(Base):
    __tablename__ = "user_link"
    __table_args__ = (
        UniqueConstraint('user_uuid', 'project_user_uuid'),
        UniqueConstraint('project_user_uuid', 'organisation_uuid')
    )
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('user_account.uuid'), nullable=False, onupdate="CASCADE")
    project_user_uuid = Column(UUID(as_uuid=True), ForeignKey('project_user.uuid'), nullable=False, onupdate="CASCADE")
    organisation_uuid = Column(UUID(as_uuid=True), ForeignKey('organisation.uuid'), onupdate="CASCADE")


class ProjectMember(Base):
    __tablename__ = "project_member"
    user_link_uuid = Column(UUID(as_uuid=True), ForeignKey('user_link.uuid'), primary_key=True, onupdate="CASCADE")
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), primary_key=True, onupdate="CASCADE")
    projects = relationship("Project", order_by=Project.name)
