from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.telefono_repository import TelefonoRepositoryImpl
from app.use_cases.telefono_use_case import TelefonoUseCase
from app.services.telefono_service import TelefonoService
from app.schemas.telefono import TelefonoCreate, TelefonoUpdate, TelefonoResponse
from app.domain.exceptions.telefono import TelefonoNoEncontrado, TelefonoDuplicado, TelefonoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/telefonos", tags=["Telefono"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TelefonoService como dependencia
def get_telefono_service(db: AsyncSession = Depends(get_db_session)) -> TelefonoService:
    repo = TelefonoRepositoryImpl(db)
    use_case = TelefonoUseCase(repo)
    return TelefonoService(use_case)

# Rutas

@router.get("/", response_model=List[TelefonoResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TelefonoService = Depends(get_telefono_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TelefonoResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TelefonoService = Depends(get_telefono_service)):
    try:
        return await service.get_by_id(id)
    except TelefonoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TelefonoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TelefonoCreate, service: TelefonoService = Depends(get_telefono_service)):
    try:
        return await service.create(data)
    except TelefonoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TelefonoInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TelefonoResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TelefonoUpdate, service: TelefonoService = Depends(get_telefono_service)):
    try:
        return await service.update(id, data)
    except TelefonoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TelefonoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TelefonoInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                    
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TelefonoService = Depends(get_telefono_service)):
    try:
        await service.delete(id)
    except TelefonoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
