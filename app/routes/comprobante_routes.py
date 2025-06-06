from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.use_cases.comprobante_use_case import ComprobanteUseCase
from app.services.comprobante_service import ComprobanteService
from app.schemas.comprobante import ComprobanteCreate, ComprobanteUpdate, ComprobanteResponse
from app.domain.exceptions.comprobante import ComprobanteNoEncontrado, ComprobanteDuplicado, ComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/comprobantes", tags=["Comprobante"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ComprobanteService como dependencia
def get_comprobante_service(db: AsyncSession = Depends(get_db_session)) -> ComprobanteService:
    repo = ComprobanteRepositoryImpl(db)
    use_case = ComprobanteUseCase(repo)
    return ComprobanteService(use_case)

# Rutas

@router.get("/", response_model=List[ComprobanteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ComprobanteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.get_by_id(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ComprobanteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ComprobanteCreate, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.create(data)
    except ComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ComprobanteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ComprobanteUpdate, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.update(id, data)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        await service.delete(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
