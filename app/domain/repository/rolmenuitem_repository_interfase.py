# ✅ app/domain/repository/rolmenuitem_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.rolmenuitem import RolMenuItem

class RolMenuItemRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, rolmenuitem_id: int) -> Optional[RolMenuItem]:
        pass

    @abstractmethod
    async def get_all(self) -> List[RolMenuItem]:
        pass

    @abstractmethod
    async def create(self, rolmenuitem: RolMenuItem) -> RolMenuItem:
        pass

    @abstractmethod
    async def update(self, rolmenuitem_id: int, rolmenuitem: RolMenuItem) -> RolMenuItem:
        pass

    @abstractmethod
    async def delete(self, rolmenuitem_id: int) -> None:
        pass
