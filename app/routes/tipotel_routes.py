from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal
from app.repositories.tipotel_repository import TipoTelRepositoryImpl
from app.use_cases.tipotel_use_case import TipoTelUseCase
from app.services.tipotel_service import TipoTelService
from app.schemas.tipotel import TipoTelCreate, TipoTelUpdate, TipoTelResponse
from app.domain.exceptions.tipotel import TipoTelNoEncontrado, TipoTelDuplicado, TipoTelInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


router = APIRouter(prefix="/tipotels", tags=["TipoTel"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# TipoTelService como dependencia
def get_tipotel_service(db: AsyncSession = Depends(get_db_session)) -> TipoTelService:
    repo = TipoTelRepositoryImpl(db)
    use_case = TipoTelUseCase(repo)
    return TipoTelService(use_case)

# Rutas

@router.get("/", response_model=List[TipoTelResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: TipoTelService = Depends(get_tipotel_service)):
    try:
        logger.info("Ruta TipoTel disparada")
        result = await service.get_all()
        logger.info(f"resultado Ruta TipoTel ::: {result}")        
        return result
    except BaseDeDatosNoDisponible as eb:
        logger.error(f"❌ Error en base de datos: {eb}")        
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio as er:
        logger.error(f"❌ Error en repositorio: {er}")
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=TipoTelResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: TipoTelService = Depends(get_tipotel_service)):
    try:
        return await service.get_by_id(id)
    except TipoTelNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=TipoTelResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: TipoTelCreate, service: TipoTelService = Depends(get_tipotel_service)):
    try:
        return await service.create(data)
    except TipoTelDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoTelInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=TipoTelResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: TipoTelUpdate, service: TipoTelService = Depends(get_tipotel_service)):
    try:
        return await service.update(id, data)
    except TipoTelNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TipoTelDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TipoTelInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))        
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: TipoTelService = Depends(get_tipotel_service)):
    try:
        await service.delete(id)
    except TipoTelNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
