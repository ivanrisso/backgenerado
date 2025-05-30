# ✅ app/services/menuitem_service.py

from typing import List
from app.use_cases.menuitem_use_case import MenuItemUseCase
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.domain.entities.menuitem import MenuItem
from app.domain.exceptions.menuitem import MenuItemNoEncontrado, MenuItemDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MenuItemService:
    def __init__(self, use_case: MenuItemUseCase):
        self.use_case = use_case

    def to_response(self, menuitem: MenuItem) -> MenuItemResponse:
        return MenuItemResponse(**menuitem.__dict__)

    async def get_by_id(self, id: int) -> MenuItemResponse:
        try:
            menuitem = await self.use_case.get_by_id(id)
            return self.to_response(menuitem)
        except MenuItemNoEncontrado as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al obtener menuitem")

    async def get_all(self) -> List[MenuItemResponse]:
        try:
            menuitems = await self.use_case.get_all()
            return [self.to_response(c) for c in menuitems]
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al listar menuitems")

    async def create(self, data: MenuItemCreate) -> MenuItemResponse:
        try:
            menuitem = await self.use_case.create(data)
            return self.to_response(menuitem)
        except (MenuItemDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear menuitem")

    async def update(self, id: int, data: MenuItemUpdate) -> MenuItemResponse:
        try:
            menuitem = await self.use_case.update(id, data)
            return self.to_response(menuitem)
        except (MenuItemNoEncontrado, MenuItemDuplicado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar menuitem")

    async def delete(self, id: int) -> None:
        try:
            await self.use_case.delete(id)
        except (MenuItemNoEncontrado, ClaveForaneaInvalida) as e:
            raise e
        except BaseDeDatosNoDisponible as e:
            raise e
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar menuitem")
