
import asyncio
import logging
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoImpuesto
from app.domain.entities.enums import TipoAplicacionEnum, BaseTributarioEnum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# General AFIP Taxes (Impuestos)
# These are different from wsfe Tributos (01, 02, etc.)
# These appear in Padron A5 getPersona results.
IMPUESTOS = [
    { "codigo_afip": "30", "nombre": "IVA", "descripcion": "Impuesto al Valor Agregado" },
    { "codigo_afip": "10", "nombre": "GANANCIAS SOCIEDADES", "descripcion": "Impuesto a las Ganancias Sociedades" },
    { "codigo_afip": "11", "nombre": "GANANCIAS PERSONAS FISICAS", "descripcion": "Impuesto a las Ganancias Personas Físicas" },
    { "codigo_afip": "20", "nombre": "MONOTRIBUTO", "descripcion": "Regimen Simplificado para Pequeños Contribuyentes" },
    { "codigo_afip": "21", "nombre": "MONOTRIBUTO AUTONOMO", "descripcion": "Regimen Simplificado - Autónomo" },
    { "codigo_afip": "301", "nombre": "EMPLEADOR-APORTES JUBILACION", "descripcion": "Régimen de Seguridad Social - Empleador" },
    { "codigo_afip": "308", "nombre": "CONTRIBUCIONES SEG.SOCIAL", "descripcion": "Contribuciones Seguridad Social" },
    { "codigo_afip": "353", "nombre": "CONTRIB. SEG.SOCIAL AUTONOMOS", "descripcion": "Contribuciones Autónomos" },
    { "codigo_afip": "32", "nombre": "IVA EXENTO", "descripcion": "IVA Exento" },
]

async def seed():
    async with SessionLocal() as db:
        from sqlalchemy import select
        
        logger.info("Starting seed of AFIP General Taxes...")
        created_count = 0
        
        for tax_data in IMPUESTOS:
            stmt = select(TipoImpuesto).where(TipoImpuesto.codigo_afip == tax_data["codigo_afip"])
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                logger.info(f"Creating tax: {tax_data['nombre']} (Code: {tax_data['codigo_afip']})")
                
                tax = TipoImpuesto(
                    codigo_afip=tax_data["codigo_afip"],
                    nombre=tax_data["nombre"],
                    descripcion=tax_data["descripcion"],
                    tipo_aplicacion=TipoAplicacionEnum.SUMA, # Default
                    base_calculo=BaseTributarioEnum.NETO_GRAVADO, # Default
                    porcentaje=0.0,
                    editable=True,
                    obligatorio=False,
                    activo=True
                )
                db.add(tax)
                created_count += 1
            else:
                 logger.info(f"Tax already exists: {tax_data['nombre']} ({tax_data['codigo_afip']})")
        
        if created_count > 0:
            await db.commit()
            
        logger.info(f"Seeding completed. Created {created_count} new entries.")

if __name__ == "__main__":
    asyncio.run(seed())
