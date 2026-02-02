from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List

from app.infrastructure.db.engine import SessionLocal
from app.repositories.usuario_repository import UsuarioRepositoryImpl
from app.repositories.rol_repository import RolRepositoryImpl
from app.use_cases.usuario_use_case import UsuarioUseCase
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.domain.exceptions.usuario import UsuarioNoEncontrado, UsuarioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

from app.core.dependencies import require_roles

router = APIRouter(prefix="/usuarios", tags=["Usuario"], dependencies=[Depends(require_roles("admin"))])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# UsuarioService como dependencia
def get_usuario_service(db: AsyncSession = Depends(get_db_session)) -> UsuarioService:
    repo = UsuarioRepositoryImpl(db)
    rol_repo = RolRepositoryImpl(db)
    use_case = UsuarioUseCase(repo, rol_repo)
    return UsuarioService(use_case)

# Rutas

@router.get("/", response_model=List[UsuarioResponse])
async def get_all(service: UsuarioService = Depends(get_usuario_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=UsuarioResponse)
async def get_by_id(id: int, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return await service.get_by_id(id)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.get("/{usuario_mail}", response_model=UsuarioResponse)
async def get_by_email(usuario_mail: str, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return await service.get_by_email(usuario_mail)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create(data: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return await service.create(data)
    except UsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=UsuarioResponse)
async def partial_update(id: int, data: UsuarioUpdate, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return await service.update(id, data)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: UsuarioService = Depends(get_usuario_service)):
    try:
        await service.delete(id)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
