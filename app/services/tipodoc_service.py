from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.schemas.tipo_doc import TipoDocCreate
from app.domain.tipodoc import TipoDoc

class TipoDocService:
    def __init__(self, db: AsyncSession):
        self.use_case = TipoDocUseCase(db)

    async def get_by_id(self, id: int) -> Optional[TipoDoc]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[TipoDoc]:
        return await self.use_case.list_all()

    async def create(self, data: TipoDocCreate) -> TipoDoc:
        return await self.use_case.create(data)