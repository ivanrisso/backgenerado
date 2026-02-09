from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from datetime import date

from app.infrastructure.db.engine import SessionLocal
from app.schemas.recibo import ReciboCreate, ReciboResponse
from app.services.recibo_service import ReciboService
from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.repositories.tipocomprobante_repository import TipoComprobanteRepositoryImpl
from app.repositories.imputacion_repository import ImputacionRepositoryImpl
from app.repositories.cuentacorriente_repository import CuentaCorrienteRepositoryImpl
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.comprobante import ComprobanteInvalido, ComprobanteNoEncontrado
from app.domain.exceptions.cliente import ClienteNoEncontrado

router = APIRouter(prefix="/recibos", tags=["Recibos"])

# DB Dependency
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# Service Dependency
def get_recibo_service(db: AsyncSession = Depends(get_db_session)) -> ReciboService:
    comp_repo = ComprobanteRepositoryImpl(db)
    tipo_repo = TipoComprobanteRepositoryImpl(db)
    imp_repo = ImputacionRepositoryImpl(db)
    cc_repo = CuentaCorrienteRepositoryImpl(db)
    cliente_repo = ClienteRepositoryImpl(db)
    return ReciboService(comp_repo, tipo_repo, imp_repo, cc_repo, cliente_repo)

@router.post("/", response_model=ReciboResponse, status_code=status.HTTP_201_CREATED)
async def create_recibo(
    data: ReciboCreate, 
    service: ReciboService = Depends(get_recibo_service)
):
    try:
        return await service.create_recibo(data)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=f"Comprobante no encontrado: {str(e)}")
    except ComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ErrorDeRepositorio as e:
        # Logged in service/repo
        raise HTTPException(status_code=500, detail="Error interno al procesar recibo")

@router.get("/", response_model=list[ReciboResponse])
async def get_recibos(
    cliente_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    limit: int = 100,
    offset: int = 0,
    service: ReciboService = Depends(get_recibo_service)
):
    return await service.get_all(
        cliente_id=cliente_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset
    )

@router.get("/{id}", response_model=ReciboResponse)
async def get_recibo_by_id(
    id: int,
    service: ReciboService = Depends(get_recibo_service)
):
    try:
        return await service.get_by_id(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=f"Recibo no encontrado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recibo(
    id: int,
    service: ReciboService = Depends(get_recibo_service)
):
    try:
        await service.delete_recibo(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail="Recibo no encontrado")
    except Exception as e:
        # Catch integrity errors etc
        raise HTTPException(status_code=500, detail=f"Error al eliminar recibo: {str(e)}")

@router.put("/{id}", response_model=ReciboResponse)
async def update_recibo(
    id: int,
    data: dict, # O crear un esquema ReciboUpdate
    service: ReciboService = Depends(get_recibo_service)
):
    try:
        return await service.update_recibo(id, data)
    except ComprobanteNoEncontrado:
        raise HTTPException(status_code=404, detail="Recibo no encontrado")

