"""Add project user attributes

Revision ID: 2c892503ce55
Revises: a0ccd222b58b
Create Date: 2021-11-15 10:17:54.162371

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2c892503ce55'
down_revision = 'a0ccd222b58b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_user_attribute',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('project_user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['project_user_uuid'], ['project_user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('project_user_uuid', 'name', 'value')
    )
    op.create_index('user_attribute_index_name_value', 'project_user_attribute', ['name', 'value'], unique=False)
    op.create_index('user_attribute_index_user_uuid_name', 'project_user_attribute', ['project_user_uuid', 'name'], unique=False)
    op.drop_column('project_user', 'refresh_token')
    op.drop_column('project_user', 'personal_access_token')
    op.drop_column('project_user', 'installation_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_user', sa.Column('installation_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('project_user', sa.Column('personal_access_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('project_user', sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index('user_attribute_index_user_uuid_name', table_name='project_user_attribute')
    op.drop_index('user_attribute_index_name_value', table_name='project_user_attribute')
    op.drop_table('project_user_attribute')
    # ### end Alembic commands ###
