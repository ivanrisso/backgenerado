from typing import  List
from app.domain.entities.rolmenuitem import RolMenuItem
from app.domain.repository.rolmenuitem_repository_interfase import RolMenuItemRepositoryInterface
from app.schemas.rolmenuitem import RolMenuItemCreate, RolMenuItemUpdate
from app.domain.exceptions.rolmenuitem import RolMenuItemNoEncontrado
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolMenuItemUseCase:
    def __init__(self, repo: RolMenuItemRepositoryInterface):
        self.repo = repo

    async def get_by_id(self, rolmenuitem_id: int) -> RolMenuItem:
        rolmenuitem = await self.repo.get_by_id(rolmenuitem_id)
        if not rolmenuitem:
            raise RolMenuItemNoEncontrado(rolmenuitem_id)
        return rolmenuitem

    async def get_all(self) -> List[RolMenuItem]:
        return await self.repo.get_all()

    async def create(self, data: RolMenuItemCreate) -> RolMenuItem:
        rolmenuitem = RolMenuItem(id=None, **data.model_dump())
        return await self.repo.create(rolmenuitem)

    async def update(self, rolmenuitem_id: int, data: RolMenuItemUpdate) -> RolMenuItem:
        existing = await self.repo.get_by_id(rolmenuitem_id)
        if not existing:
            raise RolMenuItemNoEncontrado(rolmenuitem_id)
        
        rolmenuitem = RolMenuItem(id=rolmenuitem_id, **data.model_dump(exclude_unset=True))        
        return await self.repo.update(rolmenuitem_id, rolmenuitem)

    async def delete(self, rolmenuitem_id: int) -> None:
        existing = await self.repo.get_by_id(rolmenuitem_id)
        if not existing:
            raise RolMenuItemNoEncontrado(rolmenuitem_id)

        await self.repo.delete(rolmenuitem_id)
