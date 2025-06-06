# ✅ app/services/clienteimpuesto_service.py

from typing import List
from app.use_cases.clienteimpuesto_use_case import ClienteImpuestoUseCase
from app.schemas.clienteimpuesto import ClienteImpuestoCreate, ClienteImpuestoUpdate, ClienteImpuestoResponse
from app.domain.entities.clienteimpuesto import ClienteImpuesto
from app.domain.exceptions.clienteimpuesto import ClienteImpuestoNoEncontrado, ClienteImpuestoDuplicado, ClienteImpuestoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ClienteImpuestoService:
    def __init__(self, use_case: ClienteImpuestoUseCase):
        self.use_case = use_case

    def to_response(self, clienteimpuesto: ClienteImpuesto) -> ClienteImpuestoResponse:
        return ClienteImpuestoResponse(**clienteimpuesto.__dict__)

    async def get_by_id(self, id: int) -> ClienteImpuestoResponse:
        try:
            clienteimpuesto = await self.use_case.get_by_id(id)
            return self.to_response(clienteimpuesto)
        except ClienteImpuestoNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener clienteimpuesto")

    async def get_all(self) -> List[ClienteImpuestoResponse]:
        try:
            clienteimpuestos = await self.use_case.get_all()
            return [self.to_response(c) for c in clienteimpuestos]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar clienteimpuestos")

    async def create(self, data: ClienteImpuestoCreate) -> ClienteImpuestoResponse:
        try:
            clienteimpuesto = await self.use_case.create(data)
            return self.to_response(clienteimpuesto)
        except (ClienteImpuestoDuplicado, ClaveForaneaInvalida, ClienteImpuestoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear clienteimpuesto")

    async def update(self, id: int, data: ClienteImpuestoUpdate) -> ClienteImpuestoResponse:
        try:
            clienteimpuesto = await self.use_case.update(id, data)
            return self.to_response(clienteimpuesto)
        except (ClienteImpuestoNoEncontrado, ClienteImpuestoDuplicado, ClaveForaneaInvalida, ClienteImpuestoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar clienteimpuesto")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ClienteImpuestoNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar clienteimpuesto")
