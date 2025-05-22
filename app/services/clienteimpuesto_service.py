from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.clienteimpuesto_use_case import ClienteImpuestoUseCase
from app.schemas.clienteimpuesto import ClienteImpuestoCreate
from app.infrastructure.db.orm_models import ClienteImpuesto

class ClienteImpuestoService:
    def __init__(self, db: AsyncSession):
        self.use_case = ClienteImpuestoUseCase(db)

    async def get_by_id(self, id: int) -> Optional[ClienteImpuesto]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[ClienteImpuesto]:
        return await self.use_case.list_all()

    async def create(self, data: ClienteImpuestoCreate) -> ClienteImpuesto:
        return await self.use_case.create(data)