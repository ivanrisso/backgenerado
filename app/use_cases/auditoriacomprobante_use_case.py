from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import AuditoriaComprobante
from app.repositories.auditoriacomprobante_repository import AuditoriaComprobanteRepository
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate


class AuditoriaComprobanteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = AuditoriaComprobanteRepository(db)

    async def get_by_id(self, id: int) -> Optional[AuditoriaComprobante]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[AuditoriaComprobante]:
        return await self.repo.list_all()

    async def create(self, data: AuditoriaComprobanteCreate) -> AuditoriaComprobante:
        obj = AuditoriaComprobante(**data.model_dump())
        return await self.repo.create(obj)