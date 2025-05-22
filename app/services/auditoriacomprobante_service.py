from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.auditoriacomprobante_use_case import AuditoriaComprobanteUseCase
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate
from app.domain.auditoriacomprobante import AuditoriaComprobante

class AuditoriaComprobanteService:
    def __init__(self, db: AsyncSession):
        self.use_case = AuditoriaComprobanteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[AuditoriaComprobante]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[AuditoriaComprobante]:
        return await self.use_case.list_all()

    async def create(self, data: AuditoriaComprobanteCreate) -> AuditoriaComprobante:
        return await self.use_case.create(data)