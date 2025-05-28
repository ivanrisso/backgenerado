from typing import Optional, List
from app.domain.entities.tipotel import TipoTel
from app.domain.repository.tipotel_repository_interfase import TipoTelRepositoryInterface
from app.schemas.tipotel import TipoTelCreate, TipoTelUpdate
from app.domain.exceptions.tipotel import TipoTelNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoTelUseCase:
    def __init__(self, repo: TipoTelRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, tipotel_id: int) -> TipoTel:
        tipotel = await self.repo.get_by_id(tipotel_id)
        if not tipotel:
            raise TipoTelNoEncontrado(tipotel_id)
        return tipotel

    async def get_all(self) -> List[TipoTel]:
        return await self.repo.get_all()

    async def create(self, data: TipoTelCreate) -> TipoTel:
        try:
            tipotel = TipoTel(id=None, **data.model_dump())
        except Exception as e:
            logger.exception(f"❌ Error instanciando TipoTel: {e}")
            raise
         
        return await self.repo.create(tipotel)

    async def update(self, tipotel_id: int, data: TipoTelUpdate) -> TipoTel:
        existing = await self.repo.get_by_id(tipotel_id)
        if not existing:
            raise TipoTelNoEncontrado(tipotel_id)
        
        tipotel = TipoTel(id=tipotel_id, **data.model_dump(exclude_unset=True))       
                 
        return await self.repo.update(tipotel_id, tipotel)

    async def delete(self, tipotel_id: int) -> None:
        existing = await self.repo.get_by_id(tipotel_id)
        if not existing:
            raise TipoTelNoEncontrado(tipotel_id)

        await self.repo.delete(tipotel_id)
