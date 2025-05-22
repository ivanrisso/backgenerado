from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import TipoTel
from app.repositories.tipotel_repository import TipoTelRepository
from app.schemas.tipotel import TipoTelCreate

class TipoTelUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TipoTelRepository(db)

    async def get_by_id(self, id: int) -> Optional[TipoTel]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[TipoTel]:
        return await self.repo.list_all()

    async def create(self, data: TipoTelCreate) -> TipoTel:
        obj = TipoTel(**data.model_dump())
        return await self.repo.create(obj)