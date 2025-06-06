from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepositoryImpl
from app.use_cases.cuentacorriente_use_case import CuentaCorrienteUseCase
from app.services.cuentacorriente_service import CuentaCorrienteService
from app.schemas.cuenta_corriente import CuentaCorrienteCreate, CuentaCorrienteUpdate, CuentaCorrienteResponse
from app.domain.exceptions.cuentacorriente import CuentaCorrienteNoEncontrado, CuentaCorrienteDuplicado, CuentaCorrienteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/cuentacorrientes", tags=["CuentaCorriente"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# CuentaCorrienteService como dependencia
def get_cuentacorriente_service(db: AsyncSession = Depends(get_db_session)) -> CuentaCorrienteService:
    repo = CuentaCorrienteRepositoryImpl(db)
    use_case = CuentaCorrienteUseCase(repo)
    return CuentaCorrienteService(use_case)

# Rutas

@router.get("/", response_model=List[CuentaCorrienteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: CuentaCorrienteService = Depends(get_cuentacorriente_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=CuentaCorrienteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: CuentaCorrienteService = Depends(get_cuentacorriente_service)):
    try:
        return await service.get_by_id(id)
    except CuentaCorrienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=CuentaCorrienteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: CuentaCorrienteCreate, service: CuentaCorrienteService = Depends(get_cuentacorriente_service)):
    try:
        return await service.create(data)
    except CuentaCorrienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except CuentaCorrienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                            
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=CuentaCorrienteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: CuentaCorrienteUpdate, service: CuentaCorrienteService = Depends(get_cuentacorriente_service)):
    try:
        return await service.update(id, data)
    except CuentaCorrienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CuentaCorrienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except CuentaCorrienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: CuentaCorrienteService = Depends(get_cuentacorriente_service)):
    try:
        await service.delete(id)
    except CuentaCorrienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
