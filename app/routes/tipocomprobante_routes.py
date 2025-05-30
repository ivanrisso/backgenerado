from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.tipocomprobante_repository import TipoComprobanteRepositoryImpl
from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.services.tipocomprobante_service import TipoComprobanteService
from app.schemas.tipocomprobante import TipoComprobanteCreate, TipoComprobanteUpdate, TipoComprobanteResponse
from app.domain.exceptions.tipocomprobante import TipoComprobanteNoEncontrado, TipoComprobanteDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/tipocomprobantes", tags=["TipoComprobante"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TipoComprobanteService como dependencia
def get_tipocomprobante_service(db: AsyncSession = Depends(get_db_session)) -> TipoComprobanteService:
    repo = TipoComprobanteRepositoryImpl(db)
    use_case = TipoComprobanteUseCase(repo)
    return TipoComprobanteService(use_case)

# Rutas

@router.get("/", response_model=List[TipoComprobanteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TipoComprobanteService = Depends(get_tipocomprobante_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TipoComprobanteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TipoComprobanteService = Depends(get_tipocomprobante_service)):
    try:
        return await service.get_by_id(id)
    except TipoComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TipoComprobanteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TipoComprobanteCreate, service: TipoComprobanteService = Depends(get_tipocomprobante_service)):
    try:
        return await service.create(data)
    except TipoComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TipoComprobanteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TipoComprobanteUpdate, service: TipoComprobanteService = Depends(get_tipocomprobante_service)):
    try:
        return await service.update(id, data)
    except TipoComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TipoComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TipoComprobanteService = Depends(get_tipocomprobante_service)):
    try:
        await service.delete(id)
    except TipoComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
