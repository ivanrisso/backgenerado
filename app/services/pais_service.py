# ✅ app/services/pais_service.py

from typing import List
from app.use_cases.pais_use_case import PaisUseCase
from app.schemas.pais import PaisCreate, PaisUpdate, PaisResponse
from app.domain.entities.pais import Pais
from app.domain.exceptions.pais import PaisNoEncontrado, PaisDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class PaisService:
    def __init__(self, use_case: PaisUseCase):
        self.use_case = use_case

    def to_response(self, pais: Pais) -> PaisResponse:
        return PaisResponse(**pais.__dict__)

    async def get_by_id(self, id: int) -> PaisResponse:
        try:
            pais = await self.use_case.get_by_id(id)
            return self.to_response(pais)
        except PaisNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener pais")

    async def get_all(self) -> List[PaisResponse]:
        try:
            paiss = await self.use_case.get_all()
            return [self.to_response(c) for c in paiss]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar paiss")

    async def create(self, data: PaisCreate) -> PaisResponse:
        try:
            pais = await self.use_case.create(data)
            return self.to_response(pais)
        except (PaisDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear pais")

    async def update(self, id: int, data: PaisUpdate) -> PaisResponse:
        try:
            pais = await self.use_case.update(id, data)
            return self.to_response(pais)
        except (PaisNoEncontrado, PaisDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar pais")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (PaisNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar pais")
