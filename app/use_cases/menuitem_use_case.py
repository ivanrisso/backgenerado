from typing import  List
from app.domain.entities.menuitem import MenuItem
from app.domain.repository.menuitem_repository_interfase import MenuItemRepositoryInterface
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate
from app.domain.exceptions.menuitem import MenuItemNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MenuItemUseCase:
    def __init__(self, repo: MenuItemRepositoryInterface, rol_repo):
        self.repo = repo
        self.rol_repo = rol_repo

    async def get_by_id(self, menuitem_id: int) -> MenuItem:
        menuitem = await self.repo.get_by_id(menuitem_id)
        if not menuitem:
            raise MenuItemNoEncontrado(menuitem_id)
        return menuitem

    async def get_all(self) -> List[MenuItem]:
        return await self.repo.get_all()

    async def create(self, data: MenuItemCreate) -> MenuItem:
        menuitem_data = data.model_dump(exclude={"role_ids"})
        menuitem = MenuItem(id=None, **menuitem_data)
        
        if data.role_ids:
            roles = []
            for rid in data.role_ids:
                rol = await self.rol_repo.get_by_id(rid)
                if rol:
                    roles.append(rol)
            menuitem.roles = roles

        return await self.repo.create(menuitem)

    async def update(self, menuitem_id: int, data: MenuItemUpdate) -> MenuItem:
        existing = await self.repo.get_by_id(menuitem_id)
        if not existing:
            raise MenuItemNoEncontrado(menuitem_id)
        
        update_data = data.model_dump(exclude_unset=True, exclude={"role_ids"})
        for k, v in update_data.items():
            if hasattr(existing, k):
                setattr(existing, k, v)
        
        if data.role_ids is not None:
            roles = []
            for rid in data.role_ids:
                rol = await self.rol_repo.get_by_id(rid)
                if rol:
                    roles.append(rol)
            existing.roles = roles
        
        return await self.repo.update(menuitem_id, existing)

    async def delete(self, menuitem_id: int) -> None:
        existing = await self.repo.get_by_id(menuitem_id)
        if not existing:
            raise MenuItemNoEncontrado(menuitem_id)

        await self.repo.delete(menuitem_id)
