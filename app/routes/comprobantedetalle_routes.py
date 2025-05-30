from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.comprobantedetalle_repository import ComprobanteDetalleRepositoryImpl
from app.use_cases.comprobantedetalle_use_case import ComprobanteDetalleUseCase
from app.services.comprobantedetalle_service import ComprobanteDetalleService
from app.schemas.comprobante_detalle import ComprobanteDetalleCreate, ComprobanteDetalleUpdate, ComprobanteDetalleResponse
from app.domain.exceptions.comprobantedetalle import ComprobanteDetalleNoEncontrado, ComprobanteDetalleDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/comprobantedetalles", tags=["ComprobanteDetalle"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ComprobanteDetalleService como dependencia
def get_comprobantedetalle_service(db: AsyncSession = Depends(get_db_session)) -> ComprobanteDetalleService:
    repo = ComprobanteDetalleRepositoryImpl(db)
    use_case = ComprobanteDetalleUseCase(repo)
    return ComprobanteDetalleService(use_case)

# Rutas

@router.get("/", response_model=List[ComprobanteDetalleResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ComprobanteDetalleService = Depends(get_comprobantedetalle_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ComprobanteDetalleResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ComprobanteDetalleService = Depends(get_comprobantedetalle_service)):
    try:
        return await service.get_by_id(id)
    except ComprobanteDetalleNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ComprobanteDetalleResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ComprobanteDetalleCreate, service: ComprobanteDetalleService = Depends(get_comprobantedetalle_service)):
    try:
        return await service.create(data)
    except ComprobanteDetalleDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ComprobanteDetalleResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ComprobanteDetalleUpdate, service: ComprobanteDetalleService = Depends(get_comprobantedetalle_service)):
    try:
        return await service.update(id, data)
    except ComprobanteDetalleNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ComprobanteDetalleDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ComprobanteDetalleService = Depends(get_comprobantedetalle_service)):
    try:
        await service.delete(id)
    except ComprobanteDetalleNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
