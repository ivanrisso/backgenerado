from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.operador_repository import OperadorRepositoryImpl
from app.use_cases.operador_use_case import OperadorUseCase
from app.services.operador_service import OperadorService
from app.schemas.operador import OperadorCreate, OperadorUpdate, OperadorResponse
from app.domain.exceptions.operador import OperadorNoEncontrado, OperadorDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/operadors", tags=["Operador"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# OperadorService como dependencia
def get_operador_service(db: AsyncSession = Depends(get_db_session)) -> OperadorService:
    repo = OperadorRepositoryImpl(db)
    use_case = OperadorUseCase(repo)
    return OperadorService(use_case)

# Rutas

@router.get("/", response_model=List[OperadorResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: OperadorService = Depends(get_operador_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=OperadorResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: OperadorService = Depends(get_operador_service)):
    try:
        return await service.get_by_id(id)
    except OperadorNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=OperadorResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: OperadorCreate, service: OperadorService = Depends(get_operador_service)):
    try:
        return await service.create(data)
    except OperadorDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=OperadorResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: OperadorUpdate, service: OperadorService = Depends(get_operador_service)):
    try:
        return await service.update(id, data)
    except OperadorNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OperadorDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: OperadorService = Depends(get_operador_service)):
    try:
        await service.delete(id)
    except OperadorNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
