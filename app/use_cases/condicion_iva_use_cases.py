from typing import List, Optional
from app.domain.entities.condicion_iva import CondicionIva
from app.services.condicion_iva_service import CondicionIvaService

class GetCondicionesIvaUseCase:
    def __init__(self, service: CondicionIvaService):
        self.service = service
    async def execute(self) -> List[CondicionIva]:
        return await self.service.get_all()

class GetCondicionIvaByIdUseCase:
    def __init__(self, service: CondicionIvaService):
        self.service = service
    async def execute(self, id: int) -> Optional[CondicionIva]:
        return await self.service.get_by_id(id)

class CreateCondicionIvaUseCase:
    def __init__(self, service: CondicionIvaService):
        self.service = service
    async def execute(self, entity: CondicionIva) -> CondicionIva:
        return await self.service.create(entity)

class UpdateCondicionIvaUseCase:
    def __init__(self, service: CondicionIvaService):
        self.service = service
    async def execute(self, id: int, entity: CondicionIva) -> Optional[CondicionIva]:
        return await self.service.update(id, entity)

class DeleteCondicionIvaUseCase:
    def __init__(self, service: CondicionIvaService):
        self.service = service
    async def execute(self, id: int) -> None:
        await self.service.delete(id)
