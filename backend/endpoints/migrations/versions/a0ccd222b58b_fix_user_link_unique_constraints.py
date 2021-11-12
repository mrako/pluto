"""fix user link unique constraints

Revision ID: a0ccd222b58b
Revises: f63653750ae5
Create Date: 2021-11-12 10:46:10.748651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0ccd222b58b'
down_revision = 'f63653750ae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_link_project_user_uuid_organisation_uuid_key', 'user_link', type_='unique')
    op.drop_constraint('user_link_user_uuid_project_user_uuid_key', 'user_link', type_='unique')
    op.create_unique_constraint('user_link_org_proj_user_user_key', 'user_link', ['user_uuid', 'project_user_uuid', 'organisation_uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_link', type_='unique')
    op.create_unique_constraint('user_link_user_uuid_project_user_uuid_key', 'user_link', ['user_uuid', 'project_user_uuid'])
    op.create_unique_constraint('user_link_project_user_uuid_organisation_uuid_key', 'user_link', ['project_user_uuid', 'organisation_uuid'])
    # ### end Alembic commands ###
