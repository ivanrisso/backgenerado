from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import Comprobante
from app.repositories.comprobante_repository import ComprobanteRepository
from app.schemas.comprobante import ComprobanteCreate

class ComprobanteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ComprobanteRepository(db)

    async def get_by_id(self, id: int) -> Optional[Comprobante]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[Comprobante]:
        return await self.repo.list_all()

    async def create(self, data: ComprobanteCreate) -> Comprobante:
        obj = Comprobante(**data.model_dump())
        return await self.repo.create(obj)