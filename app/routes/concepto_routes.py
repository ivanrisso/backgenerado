from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.concepto_repository import ConceptoRepositoryImpl
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.services.concepto_service import ConceptoService
from app.schemas.concepto import ConceptoCreate, ConceptoUpdate, ConceptoResponse
from app.domain.exceptions.concepto import ConceptoNoEncontrado, ConceptoDuplicado, ConceptoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/conceptos", tags=["Concepto"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ConceptoService como dependencia
def get_concepto_service(db: AsyncSession = Depends(get_db_session)) -> ConceptoService:
    repo = ConceptoRepositoryImpl(db)
    use_case = ConceptoUseCase(repo)
    return ConceptoService(use_case)

# Rutas

@router.get("/", response_model=List[ConceptoResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ConceptoService = Depends(get_concepto_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ConceptoResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ConceptoService = Depends(get_concepto_service)):
    try:
        return await service.get_by_id(id)
    except ConceptoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ConceptoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ConceptoCreate, service: ConceptoService = Depends(get_concepto_service)):
    try:
        return await service.create(data)
    except ConceptoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ConceptoInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                        
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ConceptoResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ConceptoUpdate, service: ConceptoService = Depends(get_concepto_service)):
    try:
        return await service.update(id, data)
    except ConceptoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConceptoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ConceptoInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                            
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ConceptoService = Depends(get_concepto_service)):
    try:
        await service.delete(id)
    except ConceptoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
