from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.cuentacorriente_use_case import CuentaCorrienteUseCase
from app.schemas.cuenta_corriente import CuentaCorrienteCreate
from app.domain.cuentacorriente import CuentaCorriente

class CuentaCorrienteService:
    def __init__(self, db: AsyncSession):
        self.use_case = CuentaCorrienteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[CuentaCorriente]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[CuentaCorriente]:
        return await self.use_case.list_all()

    async def create(self, data: CuentaCorrienteCreate) -> CuentaCorriente:
        return await self.use_case.create(data)