from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.menuitem_repository import MenuItemRepositoryImpl
from app.use_cases.menuitem_use_case import MenuItemUseCase
from app.services.menuitem_service import MenuItemService
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.domain.exceptions.menuitem import MenuItemNoEncontrado, MenuItemDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/menuitems", tags=["MenuItem"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# MenuItemService como dependencia
def get_menuitem_service(db: AsyncSession = Depends(get_db_session)) -> MenuItemService:
    repo = MenuItemRepositoryImpl(db)
    use_case = MenuItemUseCase(repo)
    return MenuItemService(use_case)

# Rutas

@router.get("/", response_model=List[MenuItemResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: MenuItemService = Depends(get_menuitem_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=MenuItemResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: MenuItemService = Depends(get_menuitem_service)):
    try:
        return await service.get_by_id(id)
    except MenuItemNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: MenuItemCreate, service: MenuItemService = Depends(get_menuitem_service)):
    try:
        return await service.create(data)
    except MenuItemDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=MenuItemResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: MenuItemUpdate, service: MenuItemService = Depends(get_menuitem_service)):
    try:
        return await service.update(id, data)
    except MenuItemNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MenuItemDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: MenuItemService = Depends(get_menuitem_service)):
    try:
        await service.delete(id)
    except MenuItemNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
