from typing import List, Optional
from app.use_cases.articulo_use_case import ArticuloUseCase
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate
from app.domain.entities.articulo import Articulo

class ArticuloService:
    def __init__(self, use_case: ArticuloUseCase):
        self.use_case = use_case

    async def get_all(self) -> List[Articulo]:
        return await self.use_case.get_all()

    async def get_by_id(self, id: int) -> Optional[Articulo]:
        return await self.use_case.get_by_id(id)

    async def create(self, data: ArticuloCreate) -> Articulo:
        return await self.use_case.create(data)

    async def update(self, id: int, data: ArticuloUpdate) -> Optional[Articulo]:
        return await self.use_case.update(id, data)

    async def delete(self, id: int) -> bool:
        return await self.use_case.delete(id)
