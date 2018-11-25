"""Create table sensors

Revision ID: d81d91dc0c58
Revises: 
Create Date: 2018-11-24 19:05:15.614572

"""
import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic.
revision = 'd81d91dc0c58'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sensors',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),

        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('type_id', sa.Integer, nullable=False),
        sa.Column('control_id', sa.Integer, nullable=False),
        sa.Column('deactivated', sa.Boolean),

        sa.Column('name', sa.Text, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('arduino_port', sa.Text),

        sa.Column('measurements', sa.ARRAY(sa.Integer)),
        sa.Column('pins', sa.dialects.postgresql.JSONB)
    )


def downgrade():
    op.drop_table('sensors')
