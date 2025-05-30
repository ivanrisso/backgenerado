from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.tipodom_repository import TipoDomRepositoryImpl
from app.use_cases.tipodom_use_case import TipoDomUseCase
from app.services.tipodom_service import TipoDomService
from app.schemas.tipodom import TipoDomCreate, TipoDomUpdate, TipoDomResponse
from app.domain.exceptions.tipodom import TipoDomNoEncontrado, TipoDomDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/tipodoms", tags=["TipoDom"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TipoDomService como dependencia
def get_tipodom_service(db: AsyncSession = Depends(get_db_session)) -> TipoDomService:
    repo = TipoDomRepositoryImpl(db)
    use_case = TipoDomUseCase(repo)
    return TipoDomService(use_case)

# Rutas

@router.get("/", response_model=List[TipoDomResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TipoDomService = Depends(get_tipodom_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TipoDomResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TipoDomService = Depends(get_tipodom_service)):
    try:
        return await service.get_by_id(id)
    except TipoDomNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TipoDomResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TipoDomCreate, service: TipoDomService = Depends(get_tipodom_service)):
    try:
        return await service.create(data)
    except TipoDomDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TipoDomResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TipoDomUpdate, service: TipoDomService = Depends(get_tipodom_service)):
    try:
        return await service.update(id, data)
    except TipoDomNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TipoDomDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TipoDomService = Depends(get_tipodom_service)):
    try:
        await service.delete(id)
    except TipoDomNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
