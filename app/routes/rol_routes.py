from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.rol_repository import RolRepositoryImpl
from app.use_cases.rol_use_case import RolUseCase
from app.services.rol_service import RolService
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.domain.exceptions.rol import RolNoEncontrado, RolDuplicado, RolInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/rols", tags=["Rol"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# RolService como dependencia
def get_rol_service(db: AsyncSession = Depends(get_db_session)) -> RolService:
    repo = RolRepositoryImpl(db)
    use_case = RolUseCase(repo)
    return RolService(use_case)

# Rutas

@router.get("/", response_model=List[RolResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: RolService = Depends(get_rol_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=RolResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: RolService = Depends(get_rol_service)):
    try:
        return await service.get_by_id(id)
    except RolNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: RolCreate, service: RolService = Depends(get_rol_service)):
    try:
        return await service.create(data)
    except RolDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RolInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                                            
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=RolResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: RolUpdate, service: RolService = Depends(get_rol_service)):
    try:
        return await service.update(id, data)
    except RolNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RolDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RolInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                                                                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: RolService = Depends(get_rol_service)):
    try:
        await service.delete(id)
    except RolNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
