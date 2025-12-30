#app/routes/comprobante_routes.py
from fastapi import APIRouter, Depends, status, HTTPException
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles, get_db_session

from app.infrastructure.db.engine import SessionLocal
from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.use_cases.comprobante_use_case import ComprobanteUseCase
from app.services.comprobante_service import ComprobanteService
from app.schemas.comprobante import ComprobanteCreate, ComprobanteUpdate, ComprobanteResponse
from app.domain.exceptions.comprobante import ComprobanteNoEncontrado, ComprobanteDuplicado, ComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
# ... imports
from app.use_cases.facturar_voucher_use_case import FacturarVoucherUseCase
from app.infrastructure.adapters.sql_server_voucher_repository import ExternalVoucherRepository
from app.schemas.voucher_billing import VoucherBillingRequest
from app.routes.comprobante_full_routes import get_comprobante_full_service
from app.services.comprobante_full_service import ComprobanteFullService
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.repositories.iva_repository import IvaRepositoryImpl
from app.repositories.tipoimpuesto_repository import TipoImpuestoRepositoryImpl

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comprobantes", tags=["Comprobante"])

# ... existing routes ...

# Dependency Provider for Voucher Use Case
def get_facturar_voucher_use_case(
    db: AsyncSession = Depends(get_db_session),
    full_service: ComprobanteFullService = Depends(get_comprobante_full_service)
) -> FacturarVoucherUseCase:
    # MOCK Connection String for now
    voucher_repo = ExternalVoucherRepository(connection_string="DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=VouchersDB;UID=user;PWD=pass")
    cliente_repo = ClienteRepositoryImpl(db)
    iva_repo = IvaRepositoryImpl(db)
    tipo_impuesto_repo = TipoImpuestoRepositoryImpl(db)
    
    return FacturarVoucherUseCase(
        voucher_repo, 
        full_service.use_case,
        cliente_repo,
        iva_repo,
        tipo_impuesto_repo
    )


@router.post("/from-voucher", response_model=ComprobanteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create_from_voucher(
    data: VoucherBillingRequest, 
    use_case: FacturarVoucherUseCase = Depends(get_facturar_voucher_use_case)
):
    try:
        # returns ComprobanteFull (Domain), map to ComprobanteResponse?
        # UseCase returns ComprobanteFull entity.
        # But this endpoint responses `ComprobanteResponse` (DTO).
        # We need to map it.
        # `FacturarVoucherUseCase` returns `ComprobanteFull` (entity)
        # `ComprobanteResponse` expects flattened dict usually?
        # `ComprobanteResponse` is for "flat" comprobante. `ComprobanteFullResponse` is for full.
        # Let's see what `FacturarVoucherUseCase` returns. It returns what `create_comprobante_full` returns -> `ComprobanteFull`.
        # `ComprobanteResponse` might be compatible only with `Comprobante` entity.
        # Check `ComprobanteFull` definition. It has a `comprobante` attribute which is `Comprobante`?
        # Yes, `ComprobanteFull` is Aggregate.
        # So we should return `use_case_result.comprobante` or just map manually.
        # Better yet, change response_model to `ComprobanteFullResponse` if we want full details, OR map to `ComprobanteResponse` using the header.
        
        full_entity = await use_case.execute(
            voucher_id=data.voucher_id,
            cliente_id=data.cliente_id,
            punto_venta=data.punto_venta,
            tipo_comprobante_id=data.tipo_comprobante_id,
            concepto_id=data.concepto_id
        )
        # Flatten for response if needed or use what we have.
        # Let's map to ComprobanteResponse which seems expected by this router generally.
        # We can extract the inner Comprobante + balance?
        # actually `ComprobanteResponse` mimics `Comprobante` entity.
        # `ComprobanteFull` has `.comprobante` (the header).
        # We can return `ComprobanteService.to_response(full_entity.comprobante)` ?
        # Or just return `full_entity.comprobante` and let Pydantic handle it if fields match?
        
        # Simpler: Return simple ComprobanteResponse from the header.
        return full_entity.comprobante

    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Catch-all for other errors
        raise HTTPException(status_code=500, detail=f"Error processing voucher: {str(e)}")

# ... existing routes


# ComprobanteService como dependencia
def get_comprobante_service(db: AsyncSession = Depends(get_db_session)) -> ComprobanteService:
    repo = ComprobanteRepositoryImpl(db)
    use_case = ComprobanteUseCase(repo)
    return ComprobanteService(use_case)

# Rutas

@router.get("/", response_model=List[ComprobanteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(cliente_id: int = None, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        if cliente_id:
            return await service.get_by_cliente(cliente_id)
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ComprobanteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.get_by_id(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ComprobanteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ComprobanteCreate, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.create(data)
    except ComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ComprobanteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ComprobanteUpdate, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        return await service.update(id, data)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ComprobanteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ComprobanteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))                    
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ComprobanteService = Depends(get_comprobante_service)):
    try:
        await service.delete(id)
    except ComprobanteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")
