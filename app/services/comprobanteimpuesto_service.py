from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.comprobanteimpuesto_use_case import ComprobanteImpuestoUseCase
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate
from app.infrastructure.db.orm_models import ComprobanteImpuesto

class ComprobanteImpuestoService:
    def __init__(self, db: AsyncSession):
        self.use_case = ComprobanteImpuestoUseCase(db)

    async def get_by_id(self, id: int) -> Optional[ComprobanteImpuesto]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[ComprobanteImpuesto]:
        return await self.use_case.list_all()

    async def create(self, data: ComprobanteImpuestoCreate) -> ComprobanteImpuesto:
        return await self.use_case.create(data)