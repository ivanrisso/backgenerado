from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.comprobantedetalle_use_case import ComprobanteDetalleUseCase
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate
from app.domain.comprobantedetalle import ComprobanteDetalle

class ComprobanteDetalleService:
    def __init__(self, db: AsyncSession):
        self.use_case = ComprobanteDetalleUseCase(db)

    async def get_by_id(self, id: int) -> Optional[ComprobanteDetalle]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[ComprobanteDetalle]:
        return await self.use_case.list_all()

    async def create(self, data: ComprobanteDetalleCreate) -> ComprobanteDetalle:
        return await self.use_case.create(data)