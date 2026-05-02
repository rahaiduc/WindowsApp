from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.crud import ventana as crud_ventana
from app.dependencies import DBSession
from app.models.ventana import MaterialEnum, TipoVentanaEnum
from app.schemas.ventana import (
    VentanaCreate,
    VentanaFilter,
    VentanaRead,
    VentanaUpdate,
)

router = APIRouter(prefix="/ventanas", tags=["ventanas"])


@router.get(
    "",
    response_model=list[VentanaRead],
    summary="Listar ventanas",
    description="Lista ventanas con filtros opcionales por tipo, material y rango de precio.",
)
async def list_ventanas(
    session: DBSession,
    tipo_ventana: Annotated[TipoVentanaEnum | None, Query(description="Filtrar por tipo")] = None,
    material: Annotated[MaterialEnum | None, Query(description="Filtrar por material")] = None,
    precio_min: Annotated[Decimal | None, Query(ge=0, description="Precio mínimo")] = None,
    precio_max: Annotated[Decimal | None, Query(ge=0, description="Precio máximo")] = None,
    disponible: Annotated[bool | None, Query(description="Solo disponibles")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 50,
) -> list[VentanaRead]:
    filters = VentanaFilter(
        tipo_ventana=tipo_ventana,
        material=material,
        precio_min=precio_min,
        precio_max=precio_max,
        disponible=disponible,
        skip=skip,
        limit=limit,
    )
    items = await crud_ventana.list_ventanas(session, filters)
    return [VentanaRead.model_validate(v) for v in items]


@router.get(
    "/{ventana_id}",
    response_model=VentanaRead,
    summary="Obtener una ventana por id",
    responses={404: {"description": "Ventana no encontrada"}},
)
async def get_ventana(ventana_id: int, session: DBSession) -> VentanaRead:
    ventana = await crud_ventana.get_ventana(session, ventana_id)
    if ventana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ventana no encontrada")
    return VentanaRead.model_validate(ventana)


@router.post(
    "",
    response_model=VentanaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una ventana",
    responses={409: {"description": "Ya existe una ventana con ese código"}},
)
async def create_ventana(payload: VentanaCreate, session: DBSession) -> VentanaRead:
    existing = await crud_ventana.get_ventana_by_codigo(session, payload.codigo)
    if existing is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"Ya existe una ventana con código '{payload.codigo}'",
        )
    ventana = await crud_ventana.create_ventana(session, payload)
    return VentanaRead.model_validate(ventana)


@router.put(
    "/{ventana_id}",
    response_model=VentanaRead,
    summary="Actualizar una ventana",
    responses={404: {"description": "Ventana no encontrada"}},
)
async def update_ventana(
    ventana_id: int,
    payload: VentanaUpdate,
    session: DBSession,
) -> VentanaRead:
    ventana = await crud_ventana.get_ventana(session, ventana_id)
    if ventana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ventana no encontrada")

    if payload.codigo and payload.codigo != ventana.codigo:
        clash = await crud_ventana.get_ventana_by_codigo(session, payload.codigo)
        if clash is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"Ya existe otra ventana con código '{payload.codigo}'",
            )

    updated = await crud_ventana.update_ventana(session, ventana, payload)
    return VentanaRead.model_validate(updated)


@router.delete(
    "/{ventana_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una ventana",
    responses={404: {"description": "Ventana no encontrada"}},
)
async def delete_ventana(ventana_id: int, session: DBSession) -> None:
    ventana = await crud_ventana.get_ventana(session, ventana_id)
    if ventana is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ventana no encontrada")
    await crud_ventana.delete_ventana(session, ventana)
