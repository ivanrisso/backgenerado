from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.use_cases.cliente_use_case import ClienteUseCase
from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.domain.exceptions.cliente import ClienteNoEncontrado, ClienteDuplicado, ClienteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/clientes", tags=["Cliente"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ClienteService como dependencia
def get_cliente_service(db: AsyncSession = Depends(get_db_session)) -> ClienteService:
    repo = ClienteRepositoryImpl(db)
    use_case = ClienteUseCase(repo)
    return ClienteService(use_case)

# Rutas

@router.get("/", response_model=List[ClienteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ClienteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.get_by_id(id)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.create(data)
    except ClienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))        
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ClienteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ClienteUpdate, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.update(id, data)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))            
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ClienteService = Depends(get_cliente_service)):
    try:
        await service.delete(id)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
