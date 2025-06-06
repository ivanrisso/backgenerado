# ✅ app/services/tipodoc_service.py

from typing import List
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.schemas.tipo_doc import TipoDocCreate, TipoDocUpdate, TipoDocResponse
from app.domain.entities.tipodoc import TipoDoc
from app.domain.exceptions.tipodoc import TipoDocNoEncontrado, TipoDocDuplicado, TipoDocInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoDocService:
    def __init__(self, use_case: TipoDocUseCase):
        self.use_case = use_case

    def to_response(self, tipodoc: TipoDoc) -> TipoDocResponse:
        return TipoDocResponse(**tipodoc.__dict__)

    async def get_by_id(self, id: int) -> TipoDocResponse:
        try:
            tipodoc = await self.use_case.get_by_id(id)
            return self.to_response(tipodoc)
        except TipoDocNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener tipodoc")

    async def get_all(self) -> List[TipoDocResponse]:
        try:
            tipodocs = await self.use_case.get_all()
            return [self.to_response(c) for c in tipodocs]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar tipodocs")

    async def create(self, data: TipoDocCreate) -> TipoDocResponse:
        try:
            tipodoc = await self.use_case.create(data)
            return self.to_response(tipodoc)
        except (TipoDocDuplicado, ClaveForaneaInvalida, TipoDocInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipodoc")

    async def update(self, id: int, data: TipoDocUpdate) -> TipoDocResponse:
        try:
            tipodoc = await self.use_case.update(id, data)
            return self.to_response(tipodoc)
        except (TipoDocNoEncontrado, TipoDocDuplicado, ClaveForaneaInvalida, TipoDocInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipodoc")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (TipoDocNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipodoc")
