# ✅ app/services/iva_service.py

from typing import List
from app.use_cases.iva_use_case import IvaUseCase
from app.schemas.iva import IvaCreate, IvaUpdate, IvaResponse
from app.domain.entities.iva import Iva
from app.domain.exceptions.iva import IvaNoEncontrado, IvaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida


class IvaService:
    def __init__(self, use_case: IvaUseCase):
        self.use_case = use_case

    def to_response(self, iva: Iva) -> IvaResponse:
        return IvaResponse(**iva.__dict__)

    async def get_by_id(self, id: int) -> IvaResponse:
        try:
            iva = await self.use_case.get_by_id(id)
            return self.to_response(iva)
        except IvaNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener iva")

    async def get_all(self) -> List[IvaResponse]:
        try:
            ivas = await self.use_case.get_all()
            return [self.to_response(c) for c in ivas]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar ivas")

    async def create(self, data: IvaCreate) -> IvaResponse:
        try:
            return await self.use_case.create(data)
        except (IvaDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear iva")

    async def update(self, id: int, data: IvaUpdate) -> IvaResponse:
        try:
            return await self.use_case.update(id, data)
        except (IvaNoEncontrado, IvaDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar iva")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (IvaNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar iva")
