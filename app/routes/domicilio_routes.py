from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.domicilio_repository import DomicilioRepositoryImpl
from app.use_cases.domicilio_use_case import DomicilioUseCase
from app.services.domicilio_service import DomicilioService
from app.schemas.domicilio import DomicilioCreate, DomicilioUpdate, DomicilioResponse
from app.domain.exceptions.domicilio import DomicilioNoEncontrado, DomicilioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/domicilios", tags=["Domicilio"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# DomicilioService como dependencia
def get_domicilio_service(db: AsyncSession = Depends(get_db_session)) -> DomicilioService:
    repo = DomicilioRepositoryImpl(db)
    use_case = DomicilioUseCase(repo)
    return DomicilioService(use_case)

# Rutas

@router.get("/", response_model=List[DomicilioResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: DomicilioService = Depends(get_domicilio_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=DomicilioResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: DomicilioService = Depends(get_domicilio_service)):
    try:
        return await service.get_by_id(id)
    except DomicilioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=DomicilioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: DomicilioCreate, service: DomicilioService = Depends(get_domicilio_service)):
    try:
        return await service.create(data)
    except DomicilioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=DomicilioResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: DomicilioUpdate, service: DomicilioService = Depends(get_domicilio_service)):
    try:
        return await service.update(id, data)
    except DomicilioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomicilioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: DomicilioService = Depends(get_domicilio_service)):
    try:
        await service.delete(id)
    except DomicilioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
