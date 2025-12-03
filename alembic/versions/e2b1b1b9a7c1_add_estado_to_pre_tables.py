"""add estado to preinscripcion and prepago

Revision ID: e2b1b1b9a7c1
Revises: c9d3a1f2e4b5
Create Date: 2025-11-04 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e2b1b1b9a7c1"
down_revision: Union[str, None] = "a177722917df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Be defensive: only add columns if missing (for environments where tables already include it)
    from sqlalchemy import inspect

    bind = op.get_bind()
    insp = inspect(bind)

    # preinscripcion.estado
    try:
        pre_cols = {c["name"] for c in insp.get_columns("preinscripcion")}
        if "estado" not in pre_cols:
            with op.batch_alter_table("preinscripcion", schema=None) as batch_op:
                batch_op.add_column(
                    sa.Column(
                        "estado",
                        sa.String(),
                        nullable=False,
                        server_default="pendiente",
                    )
                )
    except Exception:
        # Table might not exist in some dev states; ignore to keep migration chain progressing
        pass

    # prepago.estado
    try:
        pre_p_cols = {c["name"] for c in insp.get_columns("prepago")}
        if "estado" not in pre_p_cols:
            with op.batch_alter_table("prepago", schema=None) as batch_op:
                batch_op.add_column(
                    sa.Column(
                        "estado",
                        sa.String(),
                        nullable=False,
                        server_default="pendiente",
                    )
                )
    except Exception:
        pass


def downgrade() -> None:
    from sqlalchemy import inspect

    bind = op.get_bind()
    insp = inspect(bind)

    try:
        pre_p_cols = {c["name"] for c in insp.get_columns("prepago")}
        if "estado" in pre_p_cols:
            with op.batch_alter_table("prepago", schema=None) as batch_op:
                batch_op.drop_column("estado")
    except Exception:
        pass

    try:
        pre_cols = {c["name"] for c in insp.get_columns("preinscripcion")}
        if "estado" in pre_cols:
            with op.batch_alter_table("preinscripcion", schema=None) as batch_op:
                batch_op.drop_column("estado")
    except Exception:
        pass
