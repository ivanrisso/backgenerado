from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.use_cases.cliente_use_case import ClienteUseCase
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse


class ClienteService:
    def __init__(self, db: AsyncSession):
        self.use_case = ClienteUseCase(db)

    async def get_by_id(self, id: int) -> Optional[ClienteResponse]:
        cliente = await self.use_case.get_by_id(id)
        if cliente is None:
            return None
        return ClienteResponse(**cliente.model_dump())

    async def get_all(self) -> List[ClienteResponse]:
        clientes = await self.use_case.get_all()
        return [ClienteResponse(**c.model_dump()) for c in clientes]

    async def create(self, data: ClienteCreate) -> ClienteResponse:
        cliente = await self.use_case.create(data)
        return ClienteResponse(**cliente.model_dump())

    async def update(self, id: int, data: ClienteUpdate) -> ClienteResponse:
        cliente = await self.use_case.update(id, data)
        return ClienteResponse(**cliente.model_dump())
