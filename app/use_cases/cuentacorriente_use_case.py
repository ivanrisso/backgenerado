from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.orm_models import CuentaCorriente
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepository
from app.schemas.cuenta_corriente import CuentaCorrienteCreate

class CuentaCorrienteUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = CuentaCorrienteRepository(db)

    async def get_by_id(self, id: int) -> Optional[CuentaCorriente]:
        return await self.repo.get_by_id(id)

    async def list_all(self) -> List[CuentaCorriente]:
        return await self.repo.list_all()

    async def create(self, data: CuentaCorrienteCreate) -> CuentaCorriente:
        obj = CuentaCorriente(**data.model_dump())
        return await self.repo.create(obj)