from typing import  List
from app.domain.entities.menuitem import MenuItem
from app.domain.repository.menuitem_repository_interfase import MenuItemRepositoryInterface
from app.schemas.menuitem import MenuItemCreate, MenuItemUpdate
from app.domain.exceptions.menuitem import MenuItemNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MenuItemUseCase:
    def __init__(self, repo: MenuItemRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, menuitem_id: int) -> MenuItem:
        menuitem = await self.repo.get_by_id(menuitem_id)
        if not menuitem:
            raise MenuItemNoEncontrado(menuitem_id)
        return menuitem

    async def get_all(self) -> List[MenuItem]:
        return await self.repo.get_all()

    async def create(self, data: MenuItemCreate) -> MenuItem:
        menuitem = MenuItem(id=None, **data.model_dump())
        return await self.repo.create(menuitem)

    async def update(self, menuitem_id: int, data: MenuItemUpdate) -> MenuItem:
        existing = await self.repo.get_by_id(menuitem_id)
        if not existing:
            raise MenuItemNoEncontrado(menuitem_id)
        
        menuitem = MenuItem(id=menuitem_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(menuitem_id, menuitem)

    async def delete(self, menuitem_id: int) -> None:
        existing = await self.repo.get_by_id(menuitem_id)
        if not existing:
            raise MenuItemNoEncontrado(menuitem_id)

        await self.repo.delete(menuitem_id)
