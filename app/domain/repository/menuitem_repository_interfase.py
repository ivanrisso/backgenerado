# ✅ app/domain/repository/menuitem_repository_interface.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.menuitem import MenuItem

class MenuItemRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, menuitem_id: int) -> Optional[MenuItem]:
        pass

    @abstractmethod
    async def get_all(self) -> List[MenuItem]:
        pass

    @abstractmethod
    async def create(self, menuitem: MenuItem) -> MenuItem:
        pass

    @abstractmethod
    async def update(self, menuitem_id: int, menuitem: MenuItem) -> MenuItem:
        pass

    @abstractmethod
    async def delete(self, menuitem_id: int) -> None:
        pass
