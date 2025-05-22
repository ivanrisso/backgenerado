from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import ClienteImpuesto
from app.repositories.clienteimpuesto_repository import ClienteImpuestoRepository
from app.schemas.clienteimpuesto import ClienteImpuestoCreate

class ClienteImpuestoUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteImpuestoRepository(db)

    async def get_by_id(self, id: int) -> Optional[ClienteImpuesto]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[ClienteImpuesto]:
        return await self.repo.list_all()

    async def create(self, data: ClienteImpuestoCreate) -> ClienteImpuesto:
        obj = ClienteImpuesto(**data.model_dump())
        return await self.repo.create(obj)