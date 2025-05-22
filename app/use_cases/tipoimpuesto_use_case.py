from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import TipoImpuesto
from app.repositories.tipoimpuesto_repository import TipoImpuestoRepository
from app.schemas.tipo_impuesto import TipoImpuestoCreate

class TipoImpuestoUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = TipoImpuestoRepository(db)

    async def get_by_id(self, id: int) -> Optional[TipoImpuesto]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[TipoImpuesto]:
        return await self.repo.list_all()

    async def create(self, data: TipoImpuestoCreate) -> TipoImpuesto:
        obj = TipoImpuesto(**data.model_dump())
        return await self.repo.create(obj)