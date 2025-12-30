from typing import List, Optional
from app.domain.entities.articulo import Articulo
from app.domain.repository.articulo_repository_interfase import ArticuloRepositoryInterface
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate

class ArticuloUseCase:
    def __init__(self, repo: ArticuloRepositoryInterface):
        self.repo = repo

    async def get_all(self) -> List[Articulo]:
        return await self.repo.get_all()

    async def get_by_id(self, id: int) -> Optional[Articulo]:
        return await self.repo.get_by_id(id)

    async def create(self, data: ArticuloCreate) -> Articulo:
        articulo = Articulo(**data.model_dump())
        return await self.repo.create(articulo)

    async def update(self, id: int, data: ArticuloUpdate) -> Optional[Articulo]:
        articulo = Articulo(**data.model_dump(exclude_none=True))
        return await self.repo.update(id, articulo)

    async def delete(self, id: int) -> bool:
        return await self.repo.delete(id)
