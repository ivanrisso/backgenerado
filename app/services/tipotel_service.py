# ✅ app/services/tipotel_service.py

from typing import List
from app.use_cases.tipotel_use_case import TipoTelUseCase
from app.schemas.tipotel import TipoTelCreate, TipoTelUpdate, TipoTelResponse
from app.domain.entities.tipotel import TipoTel
from app.domain.exceptions.tipotel import TipoTelNoEncontrado, TipoTelDuplicado, TipoTelInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoTelService:
    def __init__(self, use_case: TipoTelUseCase):
        self.use_case = use_case

    def to_response(self, tipotel: TipoTel) -> TipoTelResponse:
        return TipoTelResponse(**tipotel.__dict__)

    async def get_by_id(self, id: int) -> TipoTelResponse:
        try:
            tipotel = await self.use_case.get_by_id(id)
            return self.to_response(tipotel)
        except TipoTelNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener tipotel")

    async def get_all(self) -> List[TipoTelResponse]:
        try:
            logger.info("Servicio TipoTel disparada")            
            tipotels = await self.use_case.get_all()
            logger.info(f"resultado Servicio TipoTel ::: {tipotels}")        
            return [self.to_response(c) for c in tipotels]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar tipotels")

    async def create(self, data: TipoTelCreate) -> TipoTelResponse:
        try:
            return await self.use_case.create(data)
        except (TipoTelDuplicado, ClaveForaneaInvalida, TipoTelInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipotel")

    async def update(self, id: int, data: TipoTelUpdate) -> TipoTelResponse:
        try:
            return await self.use_case.update(id, data)
        except (TipoTelNoEncontrado, TipoTelDuplicado, ClaveForaneaInvalida, TipoTelInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipotel")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TipoTelNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipotel")
