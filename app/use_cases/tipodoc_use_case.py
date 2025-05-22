from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import TipoDoc
from app.repositories.tipodoc_repository import TipoDocRepository
from app.domain.tipodoc import TipoDoc
from app.schemas.tipo_doc import TipoDocCreate

class TipoDocUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TipoDocRepository(db)

    async def get_by_id(self, id: int) -> Optional[TipoDoc]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[TipoDoc]:
        return await self.repo.list_all()

    async def create(self, data: TipoDocCreate) -> TipoDoc:
        obj = TipoDoc(**data.model_dump())
        return await self.repo.create(obj)