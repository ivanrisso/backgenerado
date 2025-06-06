from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.pais_repository import PaisRepositoryImpl
from app.use_cases.pais_use_case import PaisUseCase
from app.services.pais_service import PaisService
from app.schemas.pais import PaisCreate, PaisUpdate, PaisResponse
from app.domain.exceptions.pais import PaisNoEncontrado, PaisDuplicado, PaisInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/paiss", tags=["Pais"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# PaisService como dependencia
def get_pais_service(db: AsyncSession = Depends(get_db_session)) -> PaisService:
    repo = PaisRepositoryImpl(db)
    use_case = PaisUseCase(repo)
    return PaisService(use_case)

# Rutas

@router.get("/", response_model=List[PaisResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: PaisService = Depends(get_pais_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=PaisResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: PaisService = Depends(get_pais_service)):
    try:
        return await service.get_by_id(id)
    except PaisNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=PaisResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: PaisCreate, service: PaisService = Depends(get_pais_service)):
    try:
        return await service.create(data)
    except PaisDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PaisInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                                    
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=PaisResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: PaisUpdate, service: PaisService = Depends(get_pais_service)):
    try:
        return await service.update(id, data)
    except PaisNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PaisDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PaisInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                                        
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: PaisService = Depends(get_pais_service)):
    try:
        await service.delete(id)
    except PaisNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
