from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import TipoComprobante
from app.repositories.tipocomprobante_repository import TipoComprobanteRepository
from app.schemas.tipocomprobante import TipoComprobanteCreate

class TipoComprobanteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TipoComprobanteRepository(db)

    async def get_by_id(self, id: int) -> Optional[TipoComprobante]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[TipoComprobante]:
        return await self.repo.list_all()

    async def create(self, data: TipoComprobanteCreate) -> TipoComprobante:
        obj = TipoComprobante(**data.model_dump())
        return await self.repo.create(obj)