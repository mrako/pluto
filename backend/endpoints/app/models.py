from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
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


class Board(Base):
    __tablename__ = "board"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)


class ProjectOwner(Base):
    __tablename__ = "project_owner"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('user.uuid'), onupdate="CASCADE")
    organisation_uuid = Column(UUID(as_uuid=True), ForeignKey('organisation.uuid'), onupdate="CASCADE")
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), onupdate="CASCADE")
    projects = relationship("Project", order_by=Project.name)


class BoardOwner(Base):
    __tablename__ = "board_owner"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('project.uuid'), onupdate="CASCADE")
    repository_uuid = Column(UUID(as_uuid=True), ForeignKey('repository.uuid'), onupdate="CASCADE")
    board_uuid = Column(UUID(as_uuid=True), ForeignKey('board.uuid'), onupdate="CASCADE")
    boards = relationship("Board", order_by=Board.name)
