from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.schemas.tipocomprobante import TipoComprobanteCreate
from app.domain.tipocomprobante import TipoComprobante

class TipoComprobanteService:
    def __init__(self, db: AsyncSession):
        self.use_case = TipoComprobanteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[TipoComprobante]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[TipoComprobante]:
        return await self.use_case.list_all()

    async def create(self, data: TipoComprobanteCreate) -> TipoComprobante:
        return await self.use_case.create(data)