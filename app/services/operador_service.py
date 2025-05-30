# ✅ app/services/operador_service.py

from typing import List
from app.use_cases.operador_use_case import OperadorUseCase
from app.schemas.operador import OperadorCreate, OperadorUpdate, OperadorResponse
from app.domain.entities.operador import Operador
from app.domain.exceptions.operador import OperadorNoEncontrado, OperadorDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class OperadorService:
    def __init__(self, use_case: OperadorUseCase):
        self.use_case = use_case

    def to_response(self, operador: Operador) -> OperadorResponse:
        return OperadorResponse(**operador.__dict__)

    async def get_by_id(self, id: int) -> OperadorResponse:
        try:
            operador = await self.use_case.get_by_id(id)
            return self.to_response(operador)
        except OperadorNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener operador")

    async def get_all(self) -> List[OperadorResponse]:
        try:
            operadors = await self.use_case.get_all()
            return [self.to_response(c) for c in operadors]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar operadors")

    async def create(self, data: OperadorCreate) -> OperadorResponse:
        try:
            operador = await self.use_case.create(data)
            return self.to_response(operador)
        except (OperadorDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear operador")

    async def update(self, id: int, data: OperadorUpdate) -> OperadorResponse:
        try:
            operador = await self.use_case.update(id, data)
            return self.to_response(operador)
        except (OperadorNoEncontrado, OperadorDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar operador")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (OperadorNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar operador")
