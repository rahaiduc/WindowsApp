"""initial ventanas

Revision ID: 0001
Revises:
Create Date: 2026-05-01 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tipo_ventana_enum = postgresql.ENUM(
    "corredera", "abatible", "oscilobatiente", "fija", "pivotante",
    name="tipo_ventana_enum",
    create_type=False,
)
material_enum = postgresql.ENUM(
    "pvc", "aluminio", "madera", "mixta",
    name="material_enum",
    create_type=False,
)
tipo_vidrio_enum = postgresql.ENUM(
    "simple", "doble", "triple", "templado", "laminado",
    name="tipo_vidrio_enum",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    tipo_ventana_enum.create(bind, checkfirst=True)
    material_enum.create(bind, checkfirst=True)
    tipo_vidrio_enum.create(bind, checkfirst=True)

    op.create_table(
        "ventanas",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("codigo", sa.String(length=50), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("tipo_ventana", tipo_ventana_enum, nullable=False),
        sa.Column("material", material_enum, nullable=False),
        sa.Column("tipo_vidrio", tipo_vidrio_enum, nullable=False),
        sa.Column("color", sa.String(length=50), nullable=False, server_default="blanco"),
        sa.Column("ancho_cm", sa.Integer(), nullable=False),
        sa.Column("alto_cm", sa.Integer(), nullable=False),
        sa.Column("precio_base", sa.Numeric(10, 2), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("disponible", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("codigo", name="uq_ventanas_codigo"),
    )
    op.create_index("ix_ventanas_codigo", "ventanas", ["codigo"], unique=True)
    op.create_index("ix_ventanas_tipo_ventana", "ventanas", ["tipo_ventana"])
    op.create_index("ix_ventanas_material", "ventanas", ["material"])


def downgrade() -> None:
    op.drop_index("ix_ventanas_material", table_name="ventanas")
    op.drop_index("ix_ventanas_tipo_ventana", table_name="ventanas")
    op.drop_index("ix_ventanas_codigo", table_name="ventanas")
    op.drop_table("ventanas")

    bind = op.get_bind()
    tipo_vidrio_enum.drop(bind, checkfirst=True)
    material_enum.drop(bind, checkfirst=True)
    tipo_ventana_enum.drop(bind, checkfirst=True)
