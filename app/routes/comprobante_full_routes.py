# ✅ app/routes/comprobante_full_routes.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session, require_roles
from app.adapters.afip_adapter import AfipAdapter

from app.schemas.comprobante_full import ComprobanteFullCreate, ComprobanteFullResponse
from app.services.comprobante_full_service import ComprobanteFullService
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase
from app.repositories.comprobante_full_repository import ComprobanteFullUOW
from app.domain.exceptions.afip import ErrorAfip
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/comprobantes-full", tags=["Comprobante Full"])

# Dependency factory
def get_comprobante_full_service(
    db: AsyncSession = Depends(get_db_session)
) -> ComprobanteFullService:
    uow = ComprobanteFullUOW(db)
    afip_adapter = AfipAdapter()
    use_case = ComprobanteFullUseCase(uow=uow, afip_adapter=afip_adapter)
    return ComprobanteFullService(use_case=use_case)

# Route: POST /comprobantes-full/
@router.post(
    "/", 
    response_model=ComprobanteFullResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))]
)
async def create_comprobante_full(
    data: ComprobanteFullCreate,
    service: ComprobanteFullService = Depends(get_comprobante_full_service)
):
    try:
        return await service.create_comprobante(data)

    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))

    except ErrorAfip as e:
        raise HTTPException(status_code=502, detail=str(e))  # Bad Gateway

    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado en el backend")
