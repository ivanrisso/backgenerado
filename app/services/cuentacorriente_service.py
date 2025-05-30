# ✅ app/services/cuentacorriente_service.py

from typing import List
from app.use_cases.cuentacorriente_use_case import CuentaCorrienteUseCase
from app.schemas.cuenta_corriente import CuentaCorrienteCreate, CuentaCorrienteUpdate, CuentaCorrienteResponse
from app.domain.entities.cuentacorriente import CuentaCorriente
from app.domain.exceptions.cuentacorriente import CuentaCorrienteNoEncontrado, CuentaCorrienteDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class CuentaCorrienteService:
    def __init__(self, use_case: CuentaCorrienteUseCase):
        self.use_case = use_case

    def to_response(self, cuentacorriente: CuentaCorriente) -> CuentaCorrienteResponse:
        return CuentaCorrienteResponse(**cuentacorriente.__dict__)

    async def get_by_id(self, id: int) -> CuentaCorrienteResponse:
        try:
            cuentacorriente = await self.use_case.get_by_id(id)
            return self.to_response(cuentacorriente)
        except CuentaCorrienteNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener cuentacorriente")

    async def get_all(self) -> List[CuentaCorrienteResponse]:
        try:
            cuentacorrientes = await self.use_case.get_all()
            return [self.to_response(c) for c in cuentacorrientes]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar cuentacorrientes")

    async def create(self, data: CuentaCorrienteCreate) -> CuentaCorrienteResponse:
        try:
            cuentacorriente = await self.use_case.create(data)
            return self.to_response(cuentacorriente)
        except (CuentaCorrienteDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear cuentacorriente")

    async def update(self, id: int, data: CuentaCorrienteUpdate) -> CuentaCorrienteResponse:
        try:
            cuentacorriente = await self.use_case.update(id, data)
            return self.to_response(cuentacorriente)
        except (CuentaCorrienteNoEncontrado, CuentaCorrienteDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar cuentacorriente")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (CuentaCorrienteNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar cuentacorriente")
