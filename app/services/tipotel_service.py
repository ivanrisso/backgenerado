from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.tipotel_use_case import TipoTelUseCase
from app.schemas.tipotel import TipoTelCreate
from app.domain.tipotel import TipoTel

class TipoTelService:
    def __init__(self, db: AsyncSession):
        self.use_case = TipoTelUseCase(db)

    async def get_by_id(self, id: int) -> Optional[TipoTel]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[TipoTel]:
        return await self.use_case.list_all()

    async def create(self, data: TipoTelCreate) -> TipoTel:
        return await self.use_case.create(data)