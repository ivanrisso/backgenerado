from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.moneda_repository import MonedaRepositoryImpl
from app.use_cases.moneda_use_case import MonedaUseCase
from app.services.moneda_service import MonedaService
from app.schemas.moneda import MonedaCreate, MonedaUpdate, MonedaResponse
from app.domain.exceptions.moneda import MonedaNoEncontrado, MonedaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/monedas", tags=["Moneda"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# MonedaService como dependencia
def get_moneda_service(db: AsyncSession = Depends(get_db_session)) -> MonedaService:
    repo = MonedaRepositoryImpl(db)
    use_case = MonedaUseCase(repo)
    return MonedaService(use_case)

# Rutas

@router.get("/", response_model=List[MonedaResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: MonedaService = Depends(get_moneda_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=MonedaResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: MonedaService = Depends(get_moneda_service)):
    try:
        return await service.get_by_id(id)
    except MonedaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=MonedaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: MonedaCreate, service: MonedaService = Depends(get_moneda_service)):
    try:
        return await service.create(data)
    except MonedaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=MonedaResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: MonedaUpdate, service: MonedaService = Depends(get_moneda_service)):
    try:
        return await service.update(id, data)
    except MonedaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MonedaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: MonedaService = Depends(get_moneda_service)):
    try:
        await service.delete(id)
    except MonedaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
