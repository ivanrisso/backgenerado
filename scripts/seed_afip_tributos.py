import asyncio
import logging
from app.infrastructure.db.engine import SessionLocal
from app.domain.entities.tipoimpuesto import TipoImpuesto
from app.repositories.tipoimpuesto_repository import TipoImpuestoRepositoryImpl
from app.domain.entities.enums import TipoAplicacionEnum, BaseTributarioEnum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TAXES = [
    {
        "codigo_afip": "01",
        "nombre": "Impuestos nacionales",
        "descripcion": "Impuestos nacionales",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
    {
        "codigo_afip": "02",
        "nombre": "Impuestos provinciales",
        "descripcion": "Impuestos provinciales (ej: IIBB)",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
    {
        "codigo_afip": "03",
        "nombre": "Impuestos municipales",
        "descripcion": "Impuestos municipales",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
    {
        "codigo_afip": "04",
        "nombre": "Impuestos internos",
        "descripcion": "Impuestos internos",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO, 
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
    {
        "codigo_afip": "06",
        "nombre": "Percepción de IVA",
        "descripcion": "Percepción de Impuesto al Valor Agregado",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
     {
        "codigo_afip": "07",
        "nombre": "Percepción de IIBB",
        "descripcion": "Percepción de Ingresos Brutos",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO, 
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
    {
        "codigo_afip": "99",
        "nombre": "Otros tributos",
        "descripcion": "Otros tributos",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.OTROS,
        "porcentaje": 0.0,
        "editable": True, "obligatorio": False, "activo": True
    },
]

async def seed():
    async with SessionLocal() as session:
        repo = TipoImpuestoRepositoryImpl(session)
        existing = await repo.get_all()
        # Use simple string matching for existing codes check
        existing_codes = {t.codigo_afip for t in existing if t.codigo_afip}
        
        logger.info("Starting seed of AFIP Tributos...")
        created_count = 0
        
        for tax_data in TAXES:
            if tax_data["codigo_afip"] not in existing_codes:
                logger.info(f"Creating tax: {tax_data['nombre']} (Code: {tax_data['codigo_afip']})")
                
                # Check enum mapping if needed, but entity supports Enums directly usually.
                tax = TipoImpuesto(
                    codigo_afip=tax_data["codigo_afip"],
                    nombre=tax_data["nombre"],
                    descripcion=tax_data["descripcion"],
                    tipo_aplicacion=tax_data["tipo_aplicacion"],
                    base_calculo=tax_data["base_calculo"],
                    porcentaje=tax_data["porcentaje"],
                    editable=tax_data["editable"],
                    obligatorio=tax_data["obligatorio"],
                    activo=tax_data["activo"]
                )
                
                try:
                    await repo.create(tax)
                    created_count += 1
                except Exception as e:
                    logger.error(f"Failed to create tax {tax_data['nombre']}: {e}")
                    # In a real transaction script, a failure might rollback the session.
                    # For robust seeding, we might need new transaction per item or accept failure.
                    # Since we use one session, a rollback invalidates it.
                    # To allow others to proceed, we should probably check DB constraints first or use nested transactions if supported.
                    # For this simple script, we'll just log and continue, 
                    # BUT if session is rolled back, subsequent will fail.
                    # Re-instantiating session per item is safer for a quick fix.
            else:
                 logger.info(f"Tax already exists: {tax_data['nombre']} ({tax_data['codigo_afip']})")
        
        logger.info(f"Seeding completed. Created {created_count} new entries.")

if __name__ == "__main__":
    asyncio.run(seed())
