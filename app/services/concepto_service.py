# ✅ app/services/concepto_service.py

from typing import List
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.schemas.concepto import ConceptoCreate, ConceptoUpdate, ConceptoResponse
from app.domain.entities.concepto import Concepto
from app.domain.exceptions.concepto import ConceptoNoEncontrado, ConceptoDuplicado, ConceptoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ConceptoService:
    def __init__(self, use_case: ConceptoUseCase):
        self.use_case = use_case

    def to_response(self, concepto: Concepto) -> ConceptoResponse:
        return ConceptoResponse(**concepto.__dict__)

    async def get_by_id(self, id: int) -> ConceptoResponse:
        try:
            concepto = await self.use_case.get_by_id(id)
            return self.to_response(concepto)
        except ConceptoNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener concepto")

    async def get_all(self) -> List[ConceptoResponse]:
        try:
            conceptos = await self.use_case.get_all()
            return [self.to_response(c) for c in conceptos]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar conceptos")

    async def create(self, data: ConceptoCreate) -> ConceptoResponse:
        try:
            concepto = await self.use_case.create(data)
            return self.to_response(concepto)
        except (ConceptoDuplicado, ClaveForaneaInvalida, ConceptoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear concepto")

    async def update(self, id: int, data: ConceptoUpdate) -> ConceptoResponse:
        try:
            concepto = await self.use_case.update(id, data)
            return self.to_response(concepto)
        except (ConceptoNoEncontrado, ConceptoDuplicado, ClaveForaneaInvalida, ConceptoInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar concepto")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (ConceptoNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar concepto")
