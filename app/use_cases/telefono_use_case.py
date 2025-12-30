from typing import  List
from app.domain.entities.telefono import Telefono
from app.domain.repository.telefono_repository_interfase import TelefonoRepositoryInterface
from app.schemas.telefono import TelefonoCreate, TelefonoUpdate
from app.domain.exceptions.telefono import TelefonoNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TelefonoUseCase:
    def __init__(self, repo: TelefonoRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, telefono_id: int) -> Telefono:
        telefono = await self.repo.get_by_id(telefono_id)
        if not telefono:
            raise TelefonoNoEncontrado(telefono_id)
        return telefono

    async def get_all(self) -> List[Telefono]:
        return await self.repo.get_all()

    async def get_by_domicilio(self, domicilio_id: int) -> List[Telefono]:
        return await self.repo.get_by_domicilio(domicilio_id)

    async def create(self, data: TelefonoCreate) -> Telefono:
        telefono = Telefono(id=None, **data.model_dump())
        return await self.repo.create(telefono)

    async def update(self, telefono_id: int, data: TelefonoUpdate) -> Telefono:
        existing = await self.repo.get_by_id(telefono_id)
        if not existing:
            raise TelefonoNoEncontrado(telefono_id)
        
        telefono = Telefono(id=telefono_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(telefono_id, telefono)

    async def delete(self, telefono_id: int) -> None:
        existing = await self.repo.get_by_id(telefono_id)
        if not existing:
            raise TelefonoNoEncontrado(telefono_id)

        await self.repo.delete(telefono_id)
