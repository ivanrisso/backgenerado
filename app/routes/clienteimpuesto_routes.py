from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.clienteimpuesto_repository import ClienteImpuestoRepositoryImpl
from app.use_cases.clienteimpuesto_use_case import ClienteImpuestoUseCase
from app.services.clienteimpuesto_service import ClienteImpuestoService
from app.schemas.clienteimpuesto import ClienteImpuestoCreate, ClienteImpuestoUpdate, ClienteImpuestoResponse
from app.domain.exceptions.clienteimpuesto import ClienteImpuestoNoEncontrado, ClienteImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/clienteimpuestos", tags=["ClienteImpuesto"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ClienteImpuestoService como dependencia
def get_clienteimpuesto_service(db: AsyncSession = Depends(get_db_session)) -> ClienteImpuestoService:
    repo = ClienteImpuestoRepositoryImpl(db)
    use_case = ClienteImpuestoUseCase(repo)
    return ClienteImpuestoService(use_case)

# Rutas

@router.get("/", response_model=List[ClienteImpuestoResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ClienteImpuestoService = Depends(get_clienteimpuesto_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ClienteImpuestoResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ClienteImpuestoService = Depends(get_clienteimpuesto_service)):
    try:
        return await service.get_by_id(id)
    except ClienteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ClienteImpuestoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ClienteImpuestoCreate, service: ClienteImpuestoService = Depends(get_clienteimpuesto_service)):
    try:
        return await service.create(data)
    except ClienteImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ClienteImpuestoResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ClienteImpuestoUpdate, service: ClienteImpuestoService = Depends(get_clienteimpuesto_service)):
    try:
        return await service.update(id, data)
    except ClienteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClienteImpuestoDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ClienteImpuestoService = Depends(get_clienteimpuesto_service)):
    try:
        await service.delete(id)
    except ClienteImpuestoNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
