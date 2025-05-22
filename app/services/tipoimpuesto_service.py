from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.tipoimpuesto_use_case import TipoImpuestoUseCase
from app.schemas.tipo_impuesto import TipoImpuestoCreate
from app.domain.tipoimpuesto import TipoImpuesto

class TipoImpuestoService:
    def __init__(self, db: AsyncSession):
        self.use_case = TipoImpuestoUseCase(db)

    async def get_by_id(self, id: int) -> Optional[TipoImpuesto]:
        return await self.use_case.get_by_id(id)

    async def list_all(self) -> List[TipoImpuesto]:
        return await self.use_case.list_all()

    async def create(self, data: TipoImpuestoCreate) -> TipoImpuesto:
        return await self.use_case.create(data)