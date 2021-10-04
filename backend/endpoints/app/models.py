from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    projects = relationship(
        'Project',
        secondary='project_owner',
        cascade="save-update"
    )


class Organisation(Base):
    __tablename__ = "organisation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    projects = relationship(
        'Project',
        secondary='project_owner',
        cascade="save-update"
    )


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    boards = relationship(
        'Board',
        secondary='board_owner',
        cascade="save-update"
    )


class Repository(Base):
    __tablename__ = "repository"
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)


class ProjectOwner(Base):
    __tablename__ = "project_owner"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), onupdate="CASCADE")
    organisation_id = Column(Integer, ForeignKey('organisation.id'), onupdate="CASCADE")
    project_id = Column(Integer, ForeignKey('project.id'), onupdate="CASCADE")
    project = relationship("Project", order_by=Project.name, back_populates="owner")


Project.owners = relationship("ProjectOwner", back_populates="project")


class BoardOwner(Base):
    __tablename__ = "board_owner"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'), onupdate="CASCADE")
    repository_id = Column(Integer, ForeignKey('repository.id'), onupdate="CASCADE")
    board_id = Column(Integer, ForeignKey('board.id'), onupdate="CASCADE")
    board = relationship("Board", order_by=Board.name, back_populates="owner")


Board.owners = relationship("BoardOwner", back_populates="board")
