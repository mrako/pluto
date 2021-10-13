"""Initial db migration

Revision ID: 8812fe22bb92
Revises: 
Create Date: 2021-10-13 16:21:05.583265

"""
from uuid import UUID

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
from models import DataOrigin

revision = '8812fe22bb92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('data_origin',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('name')
    )
    op.create_table('project',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('repository',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('url')
    )
    op.create_table('user_account',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('organisation',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('data_origin_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('external_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['data_origin_uuid'], ['data_origin.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('data_origin_uuid', 'external_id'),
    sa.UniqueConstraint('data_origin_uuid', 'name')
    )
    op.create_table('project_board',
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('board_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['board_uuid'], ['board.uuid'], ),
    sa.ForeignKeyConstraint(['project_uuid'], ['project.uuid'], ),
    sa.PrimaryKeyConstraint('project_uuid', 'board_uuid')
    )
    op.create_table('project_repository',
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('repository_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['project_uuid'], ['project.uuid'], ),
    sa.ForeignKeyConstraint(['repository_uuid'], ['repository.uuid'], ),
    sa.PrimaryKeyConstraint('project_uuid', 'repository_uuid')
    )
    op.create_table('project_user',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('data_origin_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('external_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['data_origin_uuid'], ['data_origin.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('data_origin_uuid', 'external_id'),
    sa.UniqueConstraint('data_origin_uuid', 'username')
    )
    op.create_table('user_link',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('project_user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('organisation_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organisation_uuid'], ['organisation.uuid'], ),
    sa.ForeignKeyConstraint(['project_user_uuid'], ['project_user.uuid'], ),
    sa.ForeignKeyConstraint(['user_uuid'], ['user_account.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('project_user_uuid', 'organisation_uuid'),
    sa.UniqueConstraint('user_uuid', 'project_user_uuid')
    )
    op.create_table('project_owner',
    sa.Column('user_link_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('project_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['project_uuid'], ['project.uuid'], ),
    sa.ForeignKeyConstraint(['user_link_uuid'], ['user_link.uuid'], ),
    sa.PrimaryKeyConstraint('user_link_uuid', 'project_uuid')
    )
    # ### end Alembic commands ###

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.add(DataOrigin(
        uuid=UUID('40cfebc8-7d7f-42cd-a9e8-c3b80ca6c77e'),
        name='GitHub'
    ))
    session.commit()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_owner')
    op.drop_table('user_link')
    op.drop_table('project_user')
    op.drop_table('project_repository')
    op.drop_table('project_board')
    op.drop_table('organisation')
    op.drop_table('user_account')
    op.drop_table('repository')
    op.drop_table('project')
    op.drop_table('data_origin')
    op.drop_table('board')
    # ### end Alembic commands ###
