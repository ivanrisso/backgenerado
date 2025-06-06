from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.auditoriacomprobante_repository import AuditoriaComprobanteRepositoryImpl
from app.use_cases.auditoriacomprobante_use_case import AuditoriaComprobanteUseCase
from app.services.auditoriacomprobante_service import AuditoriaComprobanteService
from app.schemas.auditoria_comprobante import AuditoriaComprobanteCreate, AuditoriaComprobanteUpdate, AuditoriaComprobanteResponse
from app.domain.exceptions.auditoriacomprobante import AuditoriaComprobanteNoEncontrado, AuditoriaComprobanteDuplicado, AuditoriaComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/auditoriacomprobantes", tags=["AuditoriaComprobante"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# AuditoriaComprobanteService como dependencia
def get_auditoriacomprobante_service(db: AsyncSession = Depends(get_db_session)) -> AuditoriaComprobanteService:
    repo = AuditoriaComprobanteRepositoryImpl(db)
    use_case = AuditoriaComprobanteUseCase(repo)
    return AuditoriaComprobanteService(use_case)

# Rutas

@router.get("/", response_model=List[AuditoriaComprobanteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: AuditoriaComprobanteService = Depends(get_auditoriacomprobante_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=AuditoriaComprobanteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: AuditoriaComprobanteService = Depends(get_auditoriacomprobante_service)):
    try:
        return await service.get_by_id(id)
    except AuditoriaComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=AuditoriaComprobanteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: AuditoriaComprobanteCreate, service: AuditoriaComprobanteService = Depends(get_auditoriacomprobante_service)):
    try:
        return await service.create(data)
    except AuditoriaComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AuditoriaComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=AuditoriaComprobanteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: AuditoriaComprobanteUpdate, service: AuditoriaComprobanteService = Depends(get_auditoriacomprobante_service)):
    try:
        return await service.update(id, data)
    except AuditoriaComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AuditoriaComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AuditoriaComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                    
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: AuditoriaComprobanteService = Depends(get_auditoriacomprobante_service)):
    try:
        await service.delete(id)
    except AuditoriaComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
