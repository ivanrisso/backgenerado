from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.comprobante_use_case import ComprobanteUseCase
from app.schemas.comprobante import ComprobanteCreate
from app.domain.comprobante import Comprobante

class ComprobanteService:
    def __init__(self, db: AsyncSession):
        self.use_case = ComprobanteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[Comprobante]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[Comprobante]:
        return await self.use_case.list_all()

    async def create(self, data: ComprobanteCreate) -> Comprobante:
        return await self.use_case.create(data)