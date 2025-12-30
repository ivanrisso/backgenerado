
import logging
from typing import List, Dict, Any
from app.core.afip_client import get_padron_client
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface
from app.domain.repository.tipoimpuesto_repository_interfase import TipoImpuestoRepositoryInterface


logger = logging.getLogger(__name__)

class AfipPadronService:
    def __init__(
        self,
        cliente_repo: ClienteRepositoryInterface,
        tipo_impuesto_repo: TipoImpuestoRepositoryInterface
    ):

        self.cliente_repo = cliente_repo
        self.tipo_impuesto_repo = tipo_impuesto_repo
        self.padron = get_padron_client()

    async def get_afip_data(self, cuit: str):
        try:
            # Padron A5 getPersona
            # cuit must be int for the client usually
            response = self.padron.get_persona(int(cuit))
            return response
        except Exception as e:
            logger.error(f"Error fetching data from AFIP Padron A5 for CUIT {cuit}: {e}")
            raise

    async def compare_taxes(self, cliente_id: int):
        cliente = await self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise Exception("Cliente no encontrado")

        # 1. Fetch from AFIP
        afip_data = await self.get_afip_data(cliente.cuit)
        
        afip_taxes = []
        if hasattr(afip_data, 'personaReturn') and afip_data.personaReturn:
            p = afip_data.personaReturn
            
            # General taxes
            if hasattr(p, 'datosRegimenGeneral') and p.datosRegimenGeneral:
                taxes = getattr(p.datosRegimenGeneral, 'impuesto', [])
                for t in taxes:
                    afip_taxes.append({
                        "id": str(t.idImpuesto),
                        "nombre": t.descripcionImpuesto,
                        "fuente": "Regimen General"
                    })
            
            # Monotributo taxes
            if hasattr(p, 'datosMonotributo') and p.datosMonotributo:
                taxes = getattr(p.datosMonotributo, 'impuesto', [])
                for t in taxes:
                    # En monotributo el "impuesto" 20 es el monotributo mismo, 
                    # que suele implicar IVA incluido/no alcanzado.
                    afip_taxes.append({
                        "id": str(t.idImpuesto),
                        "nombre": t.descripcionImpuesto,
                        "fuente": "Monotributo"
                    })

        # 2. Analyze matches for IVA and IIBB
        # IVA in AFIP is usually code 30
        # IIBB in AFIP are codes 900+
        
        afip_iva = next((t for t in afip_taxes if t["id"] == "30"), None)
        afip_iibb = next((t for t in afip_taxes if t["id"] in ["900", "901", "902", "903", "904", "905", "906", "907", "908", "909"]), None)

        comparison = {
            "iva": {
                "in_afip": afip_iva is not None,
                "afip_detail": afip_iva,
                "local_match": cliente.condicion_iva_id is not None,
                "current_nombre": cliente.condicion_iva.nombre if cliente.condicion_iva else "No configurado"
            },
            "iibb": {
                "in_afip": afip_iibb is not None,
                "afip_detail": afip_iibb,
                "local_match": cliente.condicion_iibb_id is not None,
                "current_nombre": cliente.condicion_iibb.nombre if cliente.condicion_iibb else "No configurado",
                "nro_iibb": cliente.nro_iibb
            },
            "raw_afip": afip_taxes
        }

        # Determine if we should suggest changes
        comparison["missing_in_local"] = []
        if afip_iva and not cliente.condicion_iva_id:
            tipo_iva = await self.tipo_impuesto_repo.get_by_afip_code("30")
            comparison["missing_in_local"].append({
                "afip_id": "30",
                "nombre": afip_iva["nombre"],
                "tipo_impuesto_id": tipo_iva.id if tipo_iva else None,
                "target_field": "condicion_iva_id"
            })
            
        if afip_iibb and not cliente.condicion_iibb_id:
            tipo_iibb = await self.tipo_impuesto_repo.get_by_afip_code(afip_iibb["id"])
            comparison["missing_in_local"].append({
                "afip_id": afip_iibb["id"],
                "nombre": afip_iibb["nombre"],
                "tipo_impuesto_id": tipo_iibb.id if tipo_iibb else None,
                "target_field": "condicion_iibb_id"
            })

        return comparison
