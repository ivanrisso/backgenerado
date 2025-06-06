from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.localidad_repository import LocalidadRepositoryImpl
from app.use_cases.localidad_use_case import LocalidadUseCase
from app.services.localidad_service import LocalidadService
from app.schemas.localidad import LocalidadCreate, LocalidadUpdate, LocalidadResponse
from app.domain.exceptions.localidad import LocalidadNoEncontrado, LocalidadDuplicado, LocalidadInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/localidads", tags=["Localidad"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# LocalidadService como dependencia
def get_localidad_service(db: AsyncSession = Depends(get_db_session)) -> LocalidadService:
    repo = LocalidadRepositoryImpl(db)
    use_case = LocalidadUseCase(repo)
    return LocalidadService(use_case)

# Rutas

@router.get("/", response_model=List[LocalidadResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: LocalidadService = Depends(get_localidad_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=LocalidadResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: LocalidadService = Depends(get_localidad_service)):
    try:
        return await service.get_by_id(id)
    except LocalidadNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=LocalidadResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: LocalidadCreate, service: LocalidadService = Depends(get_localidad_service)):
    try:
        return await service.create(data)
    except LocalidadDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except LocalidadInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                    
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=LocalidadResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: LocalidadUpdate, service: LocalidadService = Depends(get_localidad_service)):
    try:
        return await service.update(id, data)
    except LocalidadNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LocalidadDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except LocalidadInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                        
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: LocalidadService = Depends(get_localidad_service)):
    try:
        await service.delete(id)
    except LocalidadNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
