from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
from app.core.dependencies import require_roles

from app.infrastructure.db.engine import SessionLocal, get_db
from app.repositories.cliente_repository import ClienteRepositoryImpl
from app.repositories.tipoimpuesto_repository import TipoImpuestoRepositoryImpl
from app.use_cases.cliente_use_case import ClienteUseCase
from app.services.cliente_service import ClienteService
from app.services.afip_padron_service import AfipPadronService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

from app.domain.exceptions.cliente import ClienteNoEncontrado, ClienteDuplicado, ClienteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

router = APIRouter(prefix="/clientes", tags=["Cliente"])

# DB session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# ClienteService como dependencia
def get_cliente_service(db: AsyncSession = Depends(get_db_session)) -> ClienteService:
    repo = ClienteRepositoryImpl(db)
    use_case = ClienteUseCase(repo)
    return ClienteService(use_case)

def get_afip_padron_service(db: AsyncSession = Depends(get_db_session)) -> AfipPadronService:
    cliente_repo = ClienteRepositoryImpl(db)
    tipo_impuesto_repo = TipoImpuestoRepositoryImpl(db)
    return AfipPadronService(cliente_repo, tipo_impuesto_repo)


# Rutas

@router.get("/", response_model=List[ClienteResponse], dependencies=[Depends(require_roles("admin"))])
async def get_all(service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.get_all()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

from app.schemas.cliente_deudor import ClienteDeudorResponse

@router.get("/deudores", response_model=List[ClienteDeudorResponse], dependencies=[Depends(require_roles("admin"))])
async def get_deudores(service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.get_deudores()
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}", response_model=ClienteResponse,dependencies=[Depends(require_roles("admin"))])
async def get_by_id(id: int, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.get_by_id(id)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("admin"))])
async def create(data: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.create(data)
    except ClienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))        
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.patch("/{id}", response_model=ClienteResponse, dependencies=[Depends(require_roles("admin"))])
async def partial_update(id: int, data: ClienteUpdate, service: ClienteService = Depends(get_cliente_service)):
    try:
        return await service.update(id, data)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClienteDuplicado as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ClienteInvalido as e:
        raise HTTPException(status_code=422, detail=str(e))            
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles("admin"))])
async def delete(id: int, service: ClienteService = Depends(get_cliente_service)):
    try:
        await service.delete(id)
    except ClienteNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ClaveForaneaInvalida as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BaseDeDatosNoDisponible:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    except ErrorDeRepositorio:
        raise HTTPException(status_code=500, detail="Error inesperado")

@router.get("/{id}/sync-afip-taxes", dependencies=[Depends(require_roles("admin"))])
async def compare_afip_taxes(id: int, service: AfipPadronService = Depends(get_afip_padron_service)):
    try:
        return await service.compare_taxes(id)
    except Exception as e:
        logger.exception("Error al comparar impuestos con AFIP")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{id}/sync-afip-taxes", dependencies=[Depends(require_roles("admin"))])
async def sync_afip_taxes(id: int, afip_ids: List[str], db: AsyncSession = Depends(get_db), service: AfipPadronService = Depends(get_afip_padron_service)):
    try:
        comparison = await service.compare_taxes(id)
        created_count = 0
        
        # Obtener la condición por defecto "Responsable Inscripto"
        from sqlalchemy import select
        from app.infrastructure.db.orm_models import CondicionTributaria
        stmt = select(CondicionTributaria).where(CondicionTributaria.nombre == "Responsable Inscripto")
        res = await db.execute(stmt)
        condicion_inscripto = res.scalar_one_or_none()
        default_cond_id = condicion_inscripto.id if condicion_inscripto else None

        # Filter only requested ones
        to_add = [item for item in comparison["missing_in_local"] if item["afip_id"] in afip_ids and item["tipo_impuesto_id"]]
        
        # Determine updates
        updates = {}
        for item in to_add:
            if item["target_field"] == "condicion_iva_id":
                updates["condicion_iva_id"] = default_cond_id
            elif item["target_field"] == "condicion_iibb_id":
                updates["condicion_iibb_id"] = default_cond_id
        
        if updates:
            from app.schemas.cliente import ClienteUpdate
            await service.cliente_repo.update(id, ClienteUpdate(**updates))
            created_count = len(updates)
            
        return {"status": "success", "updated_fields": list(updates.keys())}
    except Exception as e:
        logger.exception("Error al sincronizar impuestos con AFIP")
        raise HTTPException(status_code=500, detail=str(e))


