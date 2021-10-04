from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    projects = relationship(
        'Project',
        secondary='project_owner',
        cascade="save-update"
    )


class Organisation(Base):
    __tablename__ = "organisation"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, unique=True, nullable=False)
    projects = relationship(
        'Project',
        secondary='project_owner',
        cascade="save-update"
    )


class Project(Base):
    __tablename__ = "project"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    description = Column(String)
    boards = relationship(
        'Board',
        secondary='board_owner',
        cascade="save-update"
    )


class Repository(Base):
    __tablename__ = "repository"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    url = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    boards = relationship(
        'Board',
        secondary='board_owner',
        cascade="save-update"
    )


class Board(Base):
    __tablename__ = "board"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    description = Column(String)


class ProjectOwner(Base):
    __tablename__ = "project_owner"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    user_uuid = Column(UUID, ForeignKey('user.uuid'), onupdate="CASCADE")
    organisation_uuid = Column(UUID, ForeignKey('organisation.uuid'), onupdate="CASCADE")
    project_uuid = Column(UUID, ForeignKey('project.uuid'), onupdate="CASCADE")
    project = relationship("Project", order_by=Project.name, back_populates="owner")


Project.owners = relationship("ProjectOwner", back_populates="project")


class BoardOwner(Base):
    __tablename__ = "board_owner"
    uuid = Column(UUID, primary_key=True, default=uuid4())
    project_uuid = Column(UUID, ForeignKey('project.uuid'), onupdate="CASCADE")
    repository_uuid = Column(UUID, ForeignKey('repository.uuid'), onupdate="CASCADE")
    board_uuid = Column(UUID, ForeignKey('board.uuid'), onupdate="CASCADE")
    board = relationship("Board", order_by=Board.name, back_populates="owner")


Board.owners = relationship("BoardOwner", back_populates="board")
