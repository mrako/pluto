"""add Template table

Revision ID: 3328f99fdf67
Revises: a0448417b398
Create Date: 2021-10-07 12:13:36.950673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '3328f99fdf67'
down_revision = 'a0448417b398'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('template',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('template', sa.String(), nullable=False),
    sa.Column('target_name', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('url')
    )


def downgrade():
    op.drop_table('template')
