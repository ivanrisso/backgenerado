# ✅ app/services/cliente_service.py

from typing import List
from app.use_cases.cliente_use_case import ClienteUseCase
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.domain.entities.cliente import Cliente
from app.domain.exceptions.cliente import ClienteNoEncontrado, ClienteDuplicado, ClienteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ClienteService:
    def __init__(self, use_case: ClienteUseCase):
        self.use_case = use_case

    def to_response(self, cliente: Cliente) -> ClienteResponse:
        return ClienteResponse(**cliente.__dict__)

    async def get_by_id(self, id: int) -> ClienteResponse:
        try:
            cliente = await self.use_case.get_by_id(id)
            return self.to_response(cliente)
        except ClienteNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener cliente")

    async def get_all(self) -> List[ClienteResponse]:
        try:
            clientes = await self.use_case.get_all()
            return [self.to_response(c) for c in clientes]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar clientes")

    async def create(self, data: ClienteCreate) -> ClienteResponse:
        try:
            cliente = await self.use_case.create(data)
            return self.to_response(cliente)
        except (ClienteDuplicado, ClaveForaneaInvalida, ClienteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear cliente")

    async def update(self, id: int, data: ClienteUpdate) -> ClienteResponse:
        try:
            cliente = await self.use_case.update(id, data)
            return self.to_response(cliente)
        except (ClienteNoEncontrado, ClienteDuplicado, ClaveForaneaInvalida, ClienteInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar cliente")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ClienteNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar cliente")
