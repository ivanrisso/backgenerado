# ✅ app/services/domicilio_service.py

from typing import List
from app.use_cases.domicilio_use_case import DomicilioUseCase
from app.schemas.domicilio import DomicilioCreate, DomicilioUpdate, DomicilioResponse
from app.domain.entities.domicilio import Domicilio
from app.domain.exceptions.domicilio import DomicilioNoEncontrado, DomicilioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class DomicilioService:
    def __init__(self, use_case: DomicilioUseCase):
        self.use_case = use_case

    def to_response(self, domicilio: Domicilio) -> DomicilioResponse:
        return DomicilioResponse(**domicilio.__dict__)

    async def get_by_id(self, id: int) -> DomicilioResponse:
        try:
            domicilio = await self.use_case.get_by_id(id)
            return self.to_response(domicilio)
        except DomicilioNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener domicilio")

    async def get_all(self) -> List[DomicilioResponse]:
        try:
            domicilios = await self.use_case.get_all()
            return [self.to_response(c) for c in domicilios]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar domicilios")

    async def create(self, data: DomicilioCreate) -> DomicilioResponse:
        try:
            domicilio = await self.use_case.create(data)
            return self.to_response(domicilio)
        except (DomicilioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear domicilio")

    async def update(self, id: int, data: DomicilioUpdate) -> DomicilioResponse:
        try:
            domicilio = await self.use_case.update(id, data)
            return self.to_response(domicilio)
        except (DomicilioNoEncontrado, DomicilioDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar domicilio")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (DomicilioNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar domicilio")
