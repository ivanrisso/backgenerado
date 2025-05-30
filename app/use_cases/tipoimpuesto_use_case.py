from typing import  List
from app.domain.entities.tipoimpuesto import TipoImpuesto
from app.domain.repository.tipoimpuesto_repository_interfase import TipoImpuestoRepositoryInterface
from app.schemas.tipo_impuesto import TipoImpuestoCreate, TipoImpuestoUpdate
from app.domain.exceptions.tipoimpuesto import TipoImpuestoNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoImpuestoUseCase:
    def __init__(self, repo: TipoImpuestoRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, tipoimpuesto_id: int) -> TipoImpuesto:
        tipoimpuesto = await self.repo.get_by_id(tipoimpuesto_id)
        if not tipoimpuesto:
            raise TipoImpuestoNoEncontrado(tipoimpuesto_id)
        return tipoimpuesto

    async def get_all(self) -> List[TipoImpuesto]:
        return await self.repo.get_all()

    async def create(self, data: TipoImpuestoCreate) -> TipoImpuesto:
        tipoimpuesto = TipoImpuesto(id=None, **data.model_dump())
        return await self.repo.create(tipoimpuesto)

    async def update(self, tipoimpuesto_id: int, data: TipoImpuestoUpdate) -> TipoImpuesto:
        existing = await self.repo.get_by_id(tipoimpuesto_id)
        if not existing:
            raise TipoImpuestoNoEncontrado(tipoimpuesto_id)
        
        tipoimpuesto = TipoImpuesto(id=tipoimpuesto_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(tipoimpuesto_id, tipoimpuesto)

    async def delete(self, tipoimpuesto_id: int) -> None:
        existing = await self.repo.get_by_id(tipoimpuesto_id)
        if not existing:
            raise TipoImpuestoNoEncontrado(tipoimpuesto_id)

        await self.repo.delete(tipoimpuesto_id)
