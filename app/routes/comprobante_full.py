# app/web/routes/comprobante_full.py

from fastapi import APIRouter, Depends
from afip import Afip

from app.schemas.comprobante_full import ComprobanteFullCreate
from app.schemas.comprobante import ComprobanteResponse
from app.services.comprobante_full_service import ComprobanteFullService
from app.core.dependencies import get_db_session, get_afip_client_dep

router = APIRouter(prefix="/v1/comprobantes/full", tags=["Comprobantes"])

@router.post("/", response_model=ComprobanteResponse, status_code=201)
async def create_full(
    payload: ComprobanteFullCreate,
    db=Depends(get_db_session),
    afip_client: Afip = Depends(get_afip_client_dep)
):
    
    service = ComprobanteFullService(db, afip_client)
    return await service.create(payload)
