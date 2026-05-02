from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ventana import Ventana
from app.schemas.ventana import VentanaCreate, VentanaFilter, VentanaUpdate


async def get_ventana(session: AsyncSession, ventana_id: int) -> Ventana | None:
    result = await session.execute(select(Ventana).where(Ventana.id == ventana_id))
    return result.scalar_one_or_none()


async def get_ventana_by_codigo(session: AsyncSession, codigo: str) -> Ventana | None:
    result = await session.execute(select(Ventana).where(Ventana.codigo == codigo))
    return result.scalar_one_or_none()


async def list_ventanas(
    session: AsyncSession,
    filters: VentanaFilter,
) -> Sequence[Ventana]:
    stmt = select(Ventana)

    if filters.tipo_ventana is not None:
        stmt = stmt.where(Ventana.tipo_ventana == filters.tipo_ventana)
    if filters.material is not None:
        stmt = stmt.where(Ventana.material == filters.material)
    if filters.precio_min is not None:
        stmt = stmt.where(Ventana.precio_base >= filters.precio_min)
    if filters.precio_max is not None:
        stmt = stmt.where(Ventana.precio_base <= filters.precio_max)
    if filters.disponible is not None:
        stmt = stmt.where(Ventana.disponible == filters.disponible)

    stmt = stmt.order_by(Ventana.id).offset(filters.skip).limit(filters.limit)

    result = await session.execute(stmt)
    return result.scalars().all()


async def create_ventana(session: AsyncSession, payload: VentanaCreate) -> Ventana:
    ventana = Ventana(**payload.model_dump())
    session.add(ventana)
    await session.commit()
    await session.refresh(ventana)
    return ventana


async def update_ventana(
    session: AsyncSession,
    ventana: Ventana,
    payload: VentanaUpdate,
) -> Ventana:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(ventana, field, value)
    await session.commit()
    await session.refresh(ventana)
    return ventana


async def delete_ventana(session: AsyncSession, ventana: Ventana) -> None:
    await session.delete(ventana)
    await session.commit()
