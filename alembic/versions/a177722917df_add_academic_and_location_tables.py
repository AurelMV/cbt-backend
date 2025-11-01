"""add academic and location tables

Revision ID: a177722917df
Revises: b33d05fd52da
Create Date: 2025-10-30 22:59:26.336523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a177722917df'
down_revision: Union[str, Sequence[str], None] = 'b33d05fd52da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Academic tables
    op.create_table(
        'ciclo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreCiclo', sa.String(), nullable=False),
        sa.Column('fechaInicio', sa.Date(), nullable=False),
        sa.Column('fechaFin', sa.Date(), nullable=False),
        sa.Column('estado', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_ciclo_nombreCiclo'), 'ciclo', ['nombreCiclo'], unique=False)

    op.create_table(
        'grupo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreGrupo', sa.String(), nullable=False),
        sa.Column('aforo', sa.Integer(), nullable=False),
        sa.Column('estado', sa.Boolean(), nullable=False),
        sa.Column('ciclo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ciclo_id'], ['ciclo.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_grupo_nombreGrupo'), 'grupo', ['nombreGrupo'], unique=False)

    op.create_table(
        'clase',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigoClase', sa.String(), nullable=False),
        sa.Column('grupo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['grupo_id'], ['grupo.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_clase_codigoClase'), 'clase', ['codigoClase'], unique=False)

    # Location tables
    op.create_table(
        'departamento',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreDepartamento', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_departamento_nombreDepartamento'), 'departamento', ['nombreDepartamento'], unique=False)

    op.create_table(
        'provincia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreProvincia', sa.String(), nullable=False),
        sa.Column('departamento_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['departamento_id'], ['departamento.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_provincia_nombreProvincia'), 'provincia', ['nombreProvincia'], unique=False)

    op.create_table(
        'distrito',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreDistrito', sa.String(), nullable=False),
        sa.Column('provincia_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['provincia_id'], ['provincia.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_distrito_nombreDistrito'), 'distrito', ['nombreDistrito'], unique=False)

    op.create_table(
        'colegio',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombreColegio', sa.String(), nullable=False),
        sa.Column('distrito_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['distrito_id'], ['distrito.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_colegio_nombreColegio'), 'colegio', ['nombreColegio'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop in reverse FK order
    op.drop_index(op.f('ix_colegio_nombreColegio'), table_name='colegio')
    op.drop_table('colegio')

    op.drop_index(op.f('ix_distrito_nombreDistrito'), table_name='distrito')
    op.drop_table('distrito')

    op.drop_index(op.f('ix_provincia_nombreProvincia'), table_name='provincia')
    op.drop_table('provincia')

    op.drop_index(op.f('ix_departamento_nombreDepartamento'), table_name='departamento')
    op.drop_table('departamento')

    op.drop_index(op.f('ix_clase_codigoClase'), table_name='clase')
    op.drop_table('clase')

    op.drop_index(op.f('ix_grupo_nombreGrupo'), table_name='grupo')
    op.drop_table('grupo')

    op.drop_index(op.f('ix_ciclo_nombreCiclo'), table_name='ciclo')
    op.drop_table('ciclo')
