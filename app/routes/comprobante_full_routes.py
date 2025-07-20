# ✅ app/routes/comprobante_full_routes.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session, require_roles

from app.adapters.afip_adapter import AfipAdapter
from app.core.afip_client import get_afip_client  
from afip.electronic_billing import ElectronicBilling

from app.schemas.comprobante_full import ComprobanteFullCreate, ComprobanteFullResponse
from app.services.comprobante_full_service import ComprobanteFullService
from app.use_cases.comprobante_full_use_case import ComprobanteFullUseCase
from app.repositories.comprobante_full_repository import ComprobanteFullUOW
from app.domain.exceptions.afip import ErrorAfip
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

from app.repositories.comprobante_full_repository import ComprobanteFullUOW
from app.repositories.tipocomprobante_repository import TipoComprobanteRepositoryImpl
from app.repositories.concepto_repository import ConceptoRepositoryImpl
from app.repositories.tipodoc_repository import TipoDocRepositoryImpl
from app.repositories.moneda_repository import MonedaRepositoryImpl


from app.use_cases.tipocomprobante_use_case import TipoComprobanteUseCase
from app.use_cases.concepto_use_case import ConceptoUseCase
from app.use_cases.tipodoc_use_case import TipoDocUseCase
from app.use_cases.moneda_use_case import MonedaUseCase

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/comprobantes/full", tags=["Comprobante Full"])



# 🧠 Dependency factory
def get_comprobante_full_service(
    session: AsyncSession = Depends(get_db_session)
) -> ComprobanteFullService:
    
    uow = ComprobanteFullUOW(session)

    tipo_comprobante_uc = TipoComprobanteUseCase(TipoComprobanteRepositoryImpl(session))
    concepto_uc = ConceptoUseCase(ConceptoRepositoryImpl(session))
    tipodoc_uc = TipoDocUseCase(TipoDocRepositoryImpl(session))
    moneda_uc = MonedaUseCase(MonedaRepositoryImpl(session))

    # 👉 Instanciar el cliente AFIP y ElectronicBilling
    afip_sdk = get_afip_client()
    ebilling = ElectronicBilling(afip_sdk)

    afip_adapter = AfipAdapter(
        ebilling=ebilling,
        tipo_comprobante_uc=tipo_comprobante_uc,
        concepto_uc=concepto_uc,
        tipodoc_uc=tipodoc_uc,
        moneda_uc=moneda_uc
    )

    use_case = ComprobanteFullUseCase(uow=uow, afip_adapter=afip_adapter)
    return ComprobanteFullService(use_case)


# Route: POST /comprobantes/full/
@router.post(
    "/",
    response_model=ComprobanteFullResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
async def create_comprobante_full(
    data: ComprobanteFullCreate,
    service: ComprobanteFullService = Depends(get_comprobante_full_service),
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
