from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.iva_repository import IvaRepositoryImpl
from app.use_cases.iva_use_case import IvaUseCase
from app.services.iva_service import IvaService
from app.schemas.iva import IvaCreate, IvaUpdate, IvaResponse
from app.domain.exceptions.iva import IvaNoEncontrado, IvaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

router = APIRouter(prefix="/ivas", tags=["Iva"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# IvaService como dependencia
def get_iva_service(db: AsyncSession = Depends(get_db_session)) -> IvaService:
    repo = IvaRepositoryImpl(db)
    use_case = IvaUseCase(repo)
    return IvaService(use_case)

# Rutas

@router.get("/", response_model=List[IvaResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: IvaService = Depends(get_iva_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=IvaResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: IvaService = Depends(get_iva_service)):
    try:
        return await service.get_by_id(id)
    except IvaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=IvaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: IvaCreate, service: IvaService = Depends(get_iva_service)):
    try:
        return await service.create(data)
    except IvaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=IvaResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: IvaUpdate, service: IvaService = Depends(get_iva_service)):
    try:
        return await service.update(id, data)
    except IvaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IvaDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: IvaService = Depends(get_iva_service)):
    try:
        await service.delete(id)
    except IvaNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
