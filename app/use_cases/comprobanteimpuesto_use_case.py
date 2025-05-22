from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import ComprobanteImpuesto
from app.repositories.comprobanteimpuesto_repository import ComprobanteImpuestoRepository
from app.domain.comprobanteimpuesto import ComprobanteImpuesto
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate

class ComprobanteImpuestoUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ComprobanteImpuestoRepository(db)

    async def get_by_id(self, id: int) -> Optional[ComprobanteImpuesto]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[ComprobanteImpuesto]:
        return await self.repo.list_all()

    async def create(self, data: ComprobanteImpuestoCreate) -> ComprobanteImpuesto:
        obj = ComprobanteImpuesto(**data.model_dump())
        return await self.repo.create(obj)