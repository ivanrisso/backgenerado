from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import ComprobanteDetalle
from app.repositories.comprobantedetalle_repository import ComprobanteDetalleRepository
from app.domain.comprobantedetalle import ComprobanteDetalle
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate

class ComprobanteDetalleUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ComprobanteDetalleRepository(db)

    async def get_by_id(self, id: int) -> Optional[ComprobanteDetalle]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[ComprobanteDetalle]:
        return await self.repo.list_all()

    async def create(self, data: ComprobanteDetalleCreate) -> ComprobanteDetalle:
        obj = ComprobanteDetalle(**data.model_dump())
        return await self.repo.create(obj)