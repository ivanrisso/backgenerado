from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.tipodoc_repository import TipoDocRepositoryImpl
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.services.tipodoc_service import TipoDocService
from app.schemas.tipo_doc import TipoDocCreate, TipoDocUpdate, TipoDocResponse
from app.domain.exceptions.tipodoc import TipoDocNoEncontrado, TipoDocDuplicado, TipoDocInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


router = APIRouter(prefix="/tipodocs", tags=["TipoDoc"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TipoDocService como dependencia
def get_tipodoc_service(db: AsyncSession = Depends(get_db_session)) -> TipoDocService:
    repo = TipoDocRepositoryImpl(db)
    use_case = TipoDocUseCase(repo)
    return TipoDocService(use_case)

# Rutas

@router.get("/", response_model=List[TipoDocResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TipoDocService = Depends(get_tipodoc_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TipoDocResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TipoDocService = Depends(get_tipodoc_service)):
    try:
        return await service.get_by_id(id)
    except TipoDocNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TipoDocResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TipoDocCreate, service: TipoDocService = Depends(get_tipodoc_service)):
    try:
        return await service.create(data)
    except TipoDocDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoDocInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TipoDocResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TipoDocUpdate, service: TipoDocService = Depends(get_tipodoc_service)):
    try:
        return await service.update(id, data)    
    except TipoDocNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TipoDocDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoDocInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))        
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TipoDocService = Depends(get_tipodoc_service)):
    try:
        await service.delete(id)
    except TipoDocNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
