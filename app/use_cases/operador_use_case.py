from typing import  List
from app.domain.entities.operador import Operador
from app.domain.repository.operador_repository_interfase import OperadorRepositoryInterface
from app.schemas.operador import OperadorCreate, OperadorUpdate
from app.domain.exceptions.operador import OperadorNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class OperadorUseCase:
    def __init__(self, repo: OperadorRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, operador_id: int) -> Operador:
        operador = await self.repo.get_by_id(operador_id)
        if not operador:
            raise OperadorNoEncontrado(operador_id)
        return operador

    async def get_all(self) -> List[Operador]:
        return await self.repo.get_all()

    async def create(self, data: OperadorCreate) -> Operador:
        operador = Operador(id=None, **data.model_dump())
        return await self.repo.create(operador)

    async def update(self, operador_id: int, data: OperadorUpdate) -> Operador:
        existing = await self.repo.get_by_id(operador_id)
        if not existing:
            raise OperadorNoEncontrado(operador_id)
        
        operador = Operador(id=operador_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(operador_id, operador)

    async def delete(self, operador_id: int) -> None:
        existing = await self.repo.get_by_id(operador_id)
        if not existing:
            raise OperadorNoEncontrado(operador_id)

        await self.repo.delete(operador_id)
