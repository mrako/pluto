from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Organisation(Base):
    __tablename__ = "organisation"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)


class Project(Base):
    __tablename__ = "project"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)


class Repository(Base):
    __tablename__ = "repository"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    projects = relationship("Project", back_populates="repositories")


class Board(Base):
    __tablename__ = "board"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    projects = relationship("Project", back_populates="boards")


class ProjectOwner(Base):
    __tablename__ = "project_owner"
    __table_args__ = (
        UniqueConstraint('user_uuid', 'organisation_uuid', 'project_uuid'),
    )
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('user_account.uuid'), onupdate="CASCADE")
    organisation_uuid = Column(UUID(as_uuid=True), ForeignKey('organisation.uuid'), onupdate="CASCADE")
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), onupdate="CASCADE")
    projects = relationship("Project", order_by=Project.name)


class ProjectBoard(Base):
    __tablename__ = "project_board"
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), primary_key=True, onupdate="CASCADE")
    board_uuid = Column(UUID(as_uuid=True), ForeignKey('board.uuid'), primary_key=True, onupdate="CASCADE")


class ProjectRepository(Base):
    __tablename__ = "project_repository"
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), primary_key=True, onupdate="CASCADE")
    repository_uuid = Column(UUID(as_uuid=True), ForeignKey('repository.uuid'), primary_key=True, onupdate="CASCADE")


Project.repositories = relationship("Repository", order_by=Repository.name, back_populates="projects")
Project.boards = relationship("Board", order_by=Repository.name, back_populates="projects")
