# ✅ app/services/rolmenuitem_service.py

from typing import List
from app.use_cases.rolmenuitem_use_case import RolMenuItemUseCase
from app.schemas.rolmenuitem import RolMenuItemCreate, RolMenuItemUpdate, RolMenuItemResponse
from app.domain.entities.rolmenuitem import RolMenuItem
from app.domain.exceptions.rolmenuitem import RolMenuItemNoEncontrado, RolMenuItemDuplicado, RolMenuItemInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolMenuItemService:
    def __init__(self, use_case: RolMenuItemUseCase):
        self.use_case = use_case

    def to_response(self, rolmenuitem: RolMenuItem) -> RolMenuItemResponse:
        return RolMenuItemResponse(**rolmenuitem.__dict__)

    async def get_by_id(self, id: int) -> RolMenuItemResponse:
        try:
            rolmenuitem = await self.use_case.get_by_id(id)
            return self.to_response(rolmenuitem)
        except RolMenuItemNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener rolmenuitem")

    async def get_all(self) -> List[RolMenuItemResponse]:
        try:
            rolmenuitems = await self.use_case.get_all()
            return [self.to_response(c) for c in rolmenuitems]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar rolmenuitems")

    async def create(self, data: RolMenuItemCreate) -> RolMenuItemResponse:
        try:
            rolmenuitem = await self.use_case.create(data)
            return self.to_response(rolmenuitem)
        except (RolMenuItemDuplicado, ClaveForaneaInvalida, RolMenuItemInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rolmenuitem")

    async def update(self, id: int, data: RolMenuItemUpdate) -> RolMenuItemResponse:
        try:
            rolmenuitem = await self.use_case.update(id, data)
            return self.to_response(rolmenuitem)
        except (RolMenuItemNoEncontrado, RolMenuItemDuplicado, ClaveForaneaInvalida, RolMenuItemInvalido) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar rolmenuitem")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (RolMenuItemNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rolmenuitem")
