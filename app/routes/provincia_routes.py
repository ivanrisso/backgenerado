from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.provincia_repository import ProvinciaRepositoryImpl
from app.use_cases.provincia_use_case import ProvinciaUseCase
from app.services.provincia_service import ProvinciaService
from app.schemas.provincia import ProvinciaCreate, ProvinciaUpdate, ProvinciaResponse
from app.domain.exceptions.provincia import ProvinciaNoEncontrado, ProvinciaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/provincias", tags=["Provincia"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ProvinciaService como dependencia
def get_provincia_service(db: AsyncSession = Depends(get_db_session)) -> ProvinciaService:
    repo = ProvinciaRepositoryImpl(db)
    use_case = ProvinciaUseCase(repo)
    return ProvinciaService(use_case)

# Rutas

@router.get("/", response_model=List[ProvinciaResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ProvinciaService = Depends(get_provincia_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ProvinciaResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ProvinciaService = Depends(get_provincia_service)):
    try:
        return await service.get_by_id(id)
    except ProvinciaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ProvinciaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ProvinciaCreate, service: ProvinciaService = Depends(get_provincia_service)):
    try:
        return await service.create(data)
    except ProvinciaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ProvinciaResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ProvinciaUpdate, service: ProvinciaService = Depends(get_provincia_service)):
    try:
        return await service.update(id, data)
    except ProvinciaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProvinciaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ProvinciaService = Depends(get_provincia_service)):
    try:
        await service.delete(id)
    except ProvinciaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
