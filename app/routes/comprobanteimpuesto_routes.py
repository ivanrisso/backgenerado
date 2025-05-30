from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.comprobanteimpuesto_repository import ComprobanteImpuestoRepositoryImpl
from app.use_cases.comprobanteimpuesto_use_case import ComprobanteImpuestoUseCase
from app.services.comprobanteimpuesto_service import ComprobanteImpuestoService
from app.schemas.comprobante_impuesto import ComprobanteImpuestoCreate, ComprobanteImpuestoUpdate, ComprobanteImpuestoResponse
from app.domain.exceptions.comprobanteimpuesto import ComprobanteImpuestoNoEncontrado, ComprobanteImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/comprobanteimpuestos", tags=["ComprobanteImpuesto"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ComprobanteImpuestoService como dependencia
def get_comprobanteimpuesto_service(db: AsyncSession = Depends(get_db_session)) -> ComprobanteImpuestoService:
    repo = ComprobanteImpuestoRepositoryImpl(db)
    use_case = ComprobanteImpuestoUseCase(repo)
    return ComprobanteImpuestoService(use_case)

# Rutas

@router.get("/", response_model=List[ComprobanteImpuestoResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ComprobanteImpuestoService = Depends(get_comprobanteimpuesto_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ComprobanteImpuestoResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ComprobanteImpuestoService = Depends(get_comprobanteimpuesto_service)):
    try:
        return await service.get_by_id(id)
    except ComprobanteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ComprobanteImpuestoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ComprobanteImpuestoCreate, service: ComprobanteImpuestoService = Depends(get_comprobanteimpuesto_service)):
    try:
        return await service.create(data)
    except ComprobanteImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ComprobanteImpuestoResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ComprobanteImpuestoUpdate, service: ComprobanteImpuestoService = Depends(get_comprobanteimpuesto_service)):
    try:
        return await service.update(id, data)
    except ComprobanteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ComprobanteImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ComprobanteImpuestoService = Depends(get_comprobanteimpuesto_service)):
    try:
        await service.delete(id)
    except ComprobanteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
