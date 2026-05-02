from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.ventana import MaterialEnum, TipoVentanaEnum, TipoVidrioEnum


class VentanaBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "codigo": "VEN-PVC-001",
                "nombre": "Ventana corredera PVC blanca 120x100",
                "tipo_ventana": "corredera",
                "material": "pvc",
                "tipo_vidrio": "doble",
                "color": "blanco",
                "ancho_cm": 120,
                "alto_cm": 100,
                "precio_base": 189.90,
                "descripcion": "Ventana corredera de PVC con vidrio doble climalit, 2 hojas.",
                "stock": 25,
                "disponible": True,
            }
        },
    )

    codigo: str = Field(..., min_length=2, max_length=50, examples=["VEN-PVC-001"])
    nombre: str = Field(..., min_length=2, max_length=150)
    tipo_ventana: TipoVentanaEnum
    material: MaterialEnum
    tipo_vidrio: TipoVidrioEnum
    color: str = Field(default="blanco", max_length=50)
    ancho_cm: int = Field(..., gt=0, le=1000)
    alto_cm: int = Field(..., gt=0, le=1000)
    precio_base: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    descripcion: str | None = Field(default=None, max_length=2000)
    stock: int = Field(default=0, ge=0)
    disponible: bool = True


class VentanaCreate(VentanaBase):
    pass


class VentanaUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    codigo: str | None = Field(default=None, min_length=2, max_length=50)
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    tipo_ventana: TipoVentanaEnum | None = None
    material: MaterialEnum | None = None
    tipo_vidrio: TipoVidrioEnum | None = None
    color: str | None = Field(default=None, max_length=50)
    ancho_cm: int | None = Field(default=None, gt=0, le=1000)
    alto_cm: int | None = Field(default=None, gt=0, le=1000)
    precio_base: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    descripcion: str | None = Field(default=None, max_length=2000)
    stock: int | None = Field(default=None, ge=0)
    disponible: bool | None = None


class VentanaRead(VentanaBase):
    id: int
    created_at: datetime
    updated_at: datetime


class VentanaFilter(BaseModel):
    tipo_ventana: TipoVentanaEnum | None = None
    material: MaterialEnum | None = None
    precio_min: Decimal | None = Field(default=None, ge=0)
    precio_max: Decimal | None = Field(default=None, ge=0)
    disponible: bool | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=500)
