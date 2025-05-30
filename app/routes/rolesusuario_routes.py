from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.rolesusuario_repository import RolesUsuarioRepositoryImpl
from app.use_cases.rolesusuario_use_case import RolesUsuarioUseCase
from app.services.rolesusuario_service import RolesUsuarioService
from app.schemas.rolesusuario import RolesUsuarioCreate, RolesUsuarioUpdate, RolesUsuarioResponse
from app.domain.exceptions.rolesusuario import RolesUsuarioNoEncontrado, RolesUsuarioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/rolesusuarios", tags=["RolesUsuario"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# RolesUsuarioService como dependencia
def get_rolesusuario_service(db: AsyncSession = Depends(get_db_session)) -> RolesUsuarioService:
    repo = RolesUsuarioRepositoryImpl(db)
    use_case = RolesUsuarioUseCase(repo)
    return RolesUsuarioService(use_case)

# Rutas

@router.get("/", response_model=List[RolesUsuarioResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: RolesUsuarioService = Depends(get_rolesusuario_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=RolesUsuarioResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: RolesUsuarioService = Depends(get_rolesusuario_service)):
    try:
        return await service.get_by_id(id)
    except RolesUsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=RolesUsuarioResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: RolesUsuarioCreate, service: RolesUsuarioService = Depends(get_rolesusuario_service)):
    try:
        return await service.create(data)
    except RolesUsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=RolesUsuarioResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: RolesUsuarioUpdate, service: RolesUsuarioService = Depends(get_rolesusuario_service)):
    try:
        return await service.update(id, data)
    except RolesUsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RolesUsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: RolesUsuarioService = Depends(get_rolesusuario_service)):
    try:
        await service.delete(id)
    except RolesUsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
