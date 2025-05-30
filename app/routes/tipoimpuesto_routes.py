from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.tipoimpuesto_repository import TipoImpuestoRepositoryImpl
from app.use_cases.tipoimpuesto_use_case import TipoImpuestoUseCase
from app.services.tipoimpuesto_service import TipoImpuestoService
from app.schemas.tipo_impuesto import TipoImpuestoCreate, TipoImpuestoUpdate, TipoImpuestoResponse
from app.domain.exceptions.tipoimpuesto import TipoImpuestoNoEncontrado, TipoImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/tipoimpuestos", tags=["TipoImpuesto"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TipoImpuestoService como dependencia
def get_tipoimpuesto_service(db: AsyncSession = Depends(get_db_session)) -> TipoImpuestoService:
    repo = TipoImpuestoRepositoryImpl(db)
    use_case = TipoImpuestoUseCase(repo)
    return TipoImpuestoService(use_case)

# Rutas

@router.get("/", response_model=List[TipoImpuestoResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TipoImpuestoService = Depends(get_tipoimpuesto_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TipoImpuestoResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TipoImpuestoService = Depends(get_tipoimpuesto_service)):
    try:
        return await service.get_by_id(id)
    except TipoImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TipoImpuestoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TipoImpuestoCreate, service: TipoImpuestoService = Depends(get_tipoimpuesto_service)):
    try:
        return await service.create(data)
    except TipoImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TipoImpuestoResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TipoImpuestoUpdate, service: TipoImpuestoService = Depends(get_tipoimpuesto_service)):
    try:
        return await service.update(id, data)
    except TipoImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TipoImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TipoImpuestoService = Depends(get_tipoimpuesto_service)):
    try:
        await service.delete(id)
    except TipoImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
