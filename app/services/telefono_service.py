# ✅ app/services/telefono_service.py

from typing import List
from app.use_cases.telefono_use_case import TelefonoUseCase
from app.schemas.telefono import TelefonoCreate, TelefonoUpdate, TelefonoResponse
from app.domain.entities.telefono import Telefono
from app.domain.exceptions.telefono import TelefonoNoEncontrado, TelefonoDuplicado, TelefonoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TelefonoService:
    def __init__(self, use_case: TelefonoUseCase):
        self.use_case = use_case

    def to_response(self, telefono: Telefono) -> TelefonoResponse:
        return TelefonoResponse(**telefono.__dict__)

    async def get_by_id(self, id: int) -> TelefonoResponse:
        try:
            telefono = await self.use_case.get_by_id(id)
            return self.to_response(telefono)
        except TelefonoNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener telefono")

    async def get_all(self) -> List[TelefonoResponse]:
        try:
            telefonos = await self.use_case.get_all()
            return [self.to_response(c) for c in telefonos]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar telefonos")

    async def create(self, data: TelefonoCreate) -> TelefonoResponse:
        try:
            telefono = await self.use_case.create(data)
            return self.to_response(telefono)
        except (TelefonoDuplicado, ClaveForaneaInvalida, TelefonoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear telefono")

    async def update(self, id: int, data: TelefonoUpdate) -> TelefonoResponse:
        try:
            telefono = await self.use_case.update(id, data)
            return self.to_response(telefono)
        except (TelefonoNoEncontrado, TelefonoDuplicado, ClaveForaneaInvalida, TelefonoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar telefono")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TelefonoNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar telefono")
