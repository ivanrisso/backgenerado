from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles
from app.infrastructure.db.engine import SessionLocal
from app.repositories.articulo_repository import ArticuloRepositoryImpl
from app.use_cases.articulo_use_case import ArticuloUseCase
from app.services.articulo_service import ArticuloService
from app.schemas.articulo import ArticuloCreate, ArticuloUpdate, ArticuloResponse
from app.domain.exceptions.articulo import ArticuloNoEncontrado, ArticuloDuplicado, ArticuloInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

router = APIRouter(prefix="/articulos", tags=["Articulo"])

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

def get_articulo_service(db: AsyncSession = Depends(get_db_session)) -> ArticuloService:
    repo = ArticuloRepositoryImpl(db)
    use_case = ArticuloUseCase(repo)
    return ArticuloService(use_case)

@router.get("/", response_model=List[ArticuloResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ArticuloService = Depends(get_articulo_service)):
    return await service.get_all()

@router.get("/{id}", response_model=ArticuloResponse, dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ArticuloService = Depends(get_articulo_service)):
    articulo = await service.get_by_id(id)
    if not articulo:
        raise HTTPException(status_code=404, detail=f"Articulo {id} no encontrado")
    return articulo

@router.post("/", response_model=ArticuloResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ArticuloCreate, service: ArticuloService = Depends(get_articulo_service)):
    try:
        return await service.create(data)
    except ArticuloDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ArticuloInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.patch("/{id}", response_model=ArticuloResponse, dependencies=[Depends(require_roles("admin"))])
async def update(id: int, data: ArticuloUpdate, service: ArticuloService = Depends(get_articulo_service)):
    try:
        articulo = await service.update(id, data)
        if not articulo:
            raise HTTPException(status_code=404, detail=f"Articulo {id} no encontrado")
        return articulo
    except ArticuloDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ArticuloInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ArticuloService = Depends(get_articulo_service)):
    if not await service.delete(id):
        raise HTTPException(status_code=404, detail=f"Articulo {id} no encontrado")
