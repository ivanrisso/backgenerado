# ✅ app/services/tipoimpuesto_service.py

from typing import List
from app.use_cases.tipoimpuesto_use_case import TipoImpuestoUseCase
from app.schemas.tipo_impuesto import TipoImpuestoCreate, TipoImpuestoUpdate, TipoImpuestoResponse
from app.domain.entities.tipoimpuesto import TipoImpuesto
from app.domain.exceptions.tipoimpuesto import TipoImpuestoNoEncontrado, TipoImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoImpuestoService:
    def __init__(self, use_case: TipoImpuestoUseCase):
        self.use_case = use_case

    def to_response(self, tipoimpuesto: TipoImpuesto) -> TipoImpuestoResponse:
        return TipoImpuestoResponse(**tipoimpuesto.__dict__)

    async def get_by_id(self, id: int) -> TipoImpuestoResponse:
        try:
            tipoimpuesto = await self.use_case.get_by_id(id)
            return self.to_response(tipoimpuesto)
        except TipoImpuestoNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener tipoimpuesto")

    async def get_all(self) -> List[TipoImpuestoResponse]:
        try:
            tipoimpuestos = await self.use_case.get_all()
            return [self.to_response(c) for c in tipoimpuestos]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar tipoimpuestos")

    async def create(self, data: TipoImpuestoCreate) -> TipoImpuestoResponse:
        try:
            tipoimpuesto = await self.use_case.create(data)
            return self.to_response(tipoimpuesto)
        except (TipoImpuestoDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipoimpuesto")

    async def update(self, id: int, data: TipoImpuestoUpdate) -> TipoImpuestoResponse:
        try:
            tipoimpuesto = await self.use_case.update(id, data)
            return self.to_response(tipoimpuesto)
        except (TipoImpuestoNoEncontrado, TipoImpuestoDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipoimpuesto")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TipoImpuestoNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipoimpuesto")
