"""add estado to preinscripcion and prepago

Revision ID: e2b1b1b9a7c1
Revises: b33d05fd52da
Create Date: 2025-11-04 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e2b1b1b9a7c1'
down_revision: Union[str, None] = 'b33d05fd52da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('preinscripcion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.String(), nullable=False, server_default='pendiente'))
    with op.batch_alter_table('prepago', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estado', sa.String(), nullable=False, server_default='pendiente'))


def downgrade() -> None:
    with op.batch_alter_table('prepago', schema=None) as batch_op:
        batch_op.drop_column('estado')
    with op.batch_alter_table('preinscripcion', schema=None) as batch_op:
        batch_op.drop_column('estado')
