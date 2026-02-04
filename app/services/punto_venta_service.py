from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.db.orm_models import PuntoVenta
from app.schemas.punto_venta import PuntoVentaCreate, PuntoVentaUpdate

class PuntoVentaService:

    @staticmethod
    async def get_all(db: AsyncSession) -> List[PuntoVenta]:
        stmt = select(PuntoVenta).order_by(PuntoVenta.numero)
        result = await db.scalars(stmt)
        return result.all()

    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> Optional[PuntoVenta]:
        return await db.get(PuntoVenta, id)

    @staticmethod
    async def create(db: AsyncSession, data: PuntoVentaCreate) -> PuntoVenta:
        # Validate uniqueness of numero
        stmt = select(PuntoVenta).where(PuntoVenta.numero == data.numero)
        result = await db.scalars(stmt)
        existing = result.first()
        if existing:
            raise ValueError(f"Ya existe un Punto de Venta con número {data.numero}")

        db_obj = PuntoVenta(
            numero=data.numero,
            tipo=data.tipo,
            bloqueado=data.bloqueado
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, id: int, data: PuntoVentaUpdate) -> Optional[PuntoVenta]:
        db_obj = await db.get(PuntoVenta, id)
        if not db_obj:
            return None
        
        if data.numero is not None:
            # Check unique if changed
            if data.numero != db_obj.numero:
                 stmt = select(PuntoVenta).where(PuntoVenta.numero == data.numero)
                 result = await db.scalars(stmt)
                 existing = result.first()
                 if existing:
                     raise ValueError(f"Ya existe un Punto de Venta con número {data.numero}")
            db_obj.numero = data.numero

        if data.tipo is not None:
            db_obj.tipo = data.tipo
        if data.bloqueado is not None:
            db_obj.bloqueado = data.bloqueado
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> bool:
        db_obj = await db.get(PuntoVenta, id)
        if not db_obj:
            return False
        await db.delete(db_obj)
        await db.commit()
        return True
