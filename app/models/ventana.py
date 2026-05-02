import enum
from decimal import Decimal

from sqlalchemy import Boolean, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TipoVentanaEnum(str, enum.Enum):
    CORREDERA = "corredera"
    ABATIBLE = "abatible"
    OSCILOBATIENTE = "oscilobatiente"
    FIJA = "fija"
    PIVOTANTE = "pivotante"


class MaterialEnum(str, enum.Enum):
    PVC = "pvc"
    ALUMINIO = "aluminio"
    MADERA = "madera"
    MIXTA = "mixta"


class TipoVidrioEnum(str, enum.Enum):
    SIMPLE = "simple"
    DOBLE = "doble"
    TRIPLE = "triple"
    TEMPLADO = "templado"
    LAMINADO = "laminado"


class Ventana(Base, TimestampMixin):
    __tablename__ = "ventanas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    tipo_ventana: Mapped[TipoVentanaEnum] = mapped_column(
        Enum(
            TipoVentanaEnum,
            name="tipo_ventana_enum",
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
        index=True,
    )
    material: Mapped[MaterialEnum] = mapped_column(
        Enum(
            MaterialEnum,
            name="material_enum",
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
        index=True,
    )
    tipo_vidrio: Mapped[TipoVidrioEnum] = mapped_column(
        Enum(
            TipoVidrioEnum,
            name="tipo_vidrio_enum",
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(String(50), nullable=False, default="blanco")
    ancho_cm: Mapped[int] = mapped_column(Integer, nullable=False)
    alto_cm: Mapped[int] = mapped_column(Integer, nullable=False)

    precio_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<Ventana id={self.id} codigo={self.codigo!r} nombre={self.nombre!r}>"
