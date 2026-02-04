from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

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
