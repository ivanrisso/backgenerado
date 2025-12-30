
import asyncio
import logging
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoImpuesto, CondicionTributaria
from app.domain.entities.enums import (
    TipoAplicacionEnum, BaseTributarioEnum, AmbitoImpuestoEnum, 
    CategoriaImpuestoEnum, TipoUsoImpuestoEnum, MetodoCalculoImpuestoEnum, 
    AmbitoUsoImpuestoEnum, CategoriaFiscalImpuestoEnum
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONDICIONES = [
    { "nombre": "Responsable Inscripto", "descripcion": "Sujeto inscripto en el impuesto", "ambito": AmbitoImpuestoEnum.NACIONAL },
    { "nombre": "Monotributista", "descripcion": "Régimen simplificado", "ambito": AmbitoImpuestoEnum.NACIONAL },
    { "nombre": "Exento", "descripcion": "Sujeto exento por ley o certificado", "ambito": AmbitoImpuestoEnum.NACIONAL },
    { "nombre": "No Alcanzado", "descripcion": "La actividad no está alcanzada", "ambito": AmbitoImpuestoEnum.NACIONAL },
    { "nombre": "Convenio Multilateral", "descripcion": "Régimen de Convenio Multilateral (IIBB)", "ambito": AmbitoImpuestoEnum.PROVINCIAL },
    { "nombre": "Contribuyente Local", "descripcion": "Contribuyente Local (IIBB)", "ambito": AmbitoImpuestoEnum.PROVINCIAL },
]

# Definition of taxes with Odoo fields
ODOO_TAXES = [
    {
        "codigo_afip": "30",
        "nombre": "IVA 21%",
        "descripcion": "Impuesto al Valor Agregado 21%",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "ambito": AmbitoImpuestoEnum.NACIONAL,
        "categoria": CategoriaImpuestoEnum.IMPUESTO_DIRECTO,
        "porcentaje": 21.0,
        "tipo_uso": TipoUsoImpuestoEnum.VENTAS,
        "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
        "ambito_uso": AmbitoUsoImpuestoEnum.AMBOS,
        "importe": 21.0,
        "etiqueta_factura": "IVA 21%",
        "incluido_precio": False,
        "afecta_base_subsecuente": False,
        "categoria_fiscal": CategoriaFiscalImpuestoEnum.S,
        "notas_legales": "IVA Ventas Alícuota General",
    },
    {
        "codigo_afip": "32",
        "nombre": "IVA 10.5%",
        "descripcion": "Impuesto al Valor Agregado 10.5%",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "ambito": AmbitoImpuestoEnum.NACIONAL,
        "categoria": CategoriaImpuestoEnum.IMPUESTO_DIRECTO,
        "porcentaje": 10.5,
        "tipo_uso": TipoUsoImpuestoEnum.VENTAS,
        "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
        "ambito_uso": AmbitoUsoImpuestoEnum.AMBOS,
        "importe": 10.5,
        "etiqueta_factura": "IVA 10.5%",
        "incluido_precio": False,
        "afecta_base_subsecuente": False,
        "categoria_fiscal": CategoriaFiscalImpuestoEnum.S,
        "notas_legales": "IVA Ventas Alícuota Reducida",
    },
    {
        "codigo_afip": "900",
        "nombre": "IIBB Percepción Misiones",
        "descripcion": "Ingresos Brutos Misiones (Percepción)",
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "ambito": AmbitoImpuestoEnum.PROVINCIAL,
        "categoria": CategoriaImpuestoEnum.PERCEPCION,
        "porcentaje": 3.31,
        "tipo_uso": TipoUsoImpuestoEnum.VENTAS,
        "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
        "ambito_uso": AmbitoUsoImpuestoEnum.BIENES,
        "importe": 3.31,
        "etiqueta_factura": "Perc. IIBB MNES",
        "incluido_precio": False,
        "afecta_base_subsecuente": False,
        "categoria_fiscal": CategoriaFiscalImpuestoEnum.L,
        "notas_legales": "Percepción s/RG 02/2010",
    }
]

async def seed():
    async with SessionLocal() as db:
        
        # 1. Seed Condiciones
        logger.info("Seeding CondicionTributaria...")
        for c in CONDICIONES:
            stmt = select(CondicionTributaria).where(CondicionTributaria.nombre == c["nombre"])
            result = await db.execute(stmt)
            cond = result.scalar_one_or_none()
            
            if not cond:
                cond = CondicionTributaria(
                    nombre=c["nombre"], 
                    descripcion=c["descripcion"],
                    ambito=c["ambito"]
                )
                db.add(cond)
            else:
                cond.ambito = c["ambito"]
        
        await db.flush()

        # 2. Seed/Update Odoo Taxes
        logger.info("Seeding Odoo-aligned Taxes...")
        for tax_data in ODOO_TAXES:
            stmt = select(TipoImpuesto).where(TipoImpuesto.codigo_afip == tax_data["codigo_afip"])
            result = await db.execute(stmt)
            tax = result.scalar_one_or_none()
            
            if not tax:
                tax = TipoImpuesto(**tax_data)
                db.add(tax)
            else:
                # Update existing
                for key, value in tax_data.items():
                    setattr(tax, key, value)
        
        await db.commit()

        # 3. Associate Conditions to Taxes (1-to-N)
        logger.info("Associating Conditions to Taxes (1-to-N)...")
        
        # Helper to get tax by code
        async def get_tax_id(code):
            stmt = select(TipoImpuesto.id).where(TipoImpuesto.codigo_afip == code)
            res = await db.execute(stmt)
            return res.scalar_one_or_none()

        iva_id = await get_tax_id("30") # IVA 21%
        iibb_id = await get_tax_id("900") # IIBB Misiones

        if not iva_id:
             logger.warning("Allocating conditions: IVA 21% not found. Searching by name...")
             stmt = select(TipoImpuesto.id).where(TipoImpuesto.nombre.ilike("%IVA 21%%"))
             res = await db.execute(stmt)
             iva_id = res.scalar_one_or_none()
        
        mapping = {
            "Responsable Inscripto": iva_id,
            "Monotributista": iva_id,
            "Exento": iva_id,
            "No Alcanzado": iva_id,
            "Convenio Multilateral": iibb_id,
            "Contribuyente Local": iibb_id
        }

        stmt_conds = select(CondicionTributaria)
        result_conds = await db.execute(stmt_conds)
        all_conds = result_conds.scalars().all()
        
        for cond in all_conds:
            if cond.nombre in mapping:
                target_tax_id = mapping[cond.nombre]
                if target_tax_id:
                    cond.tipo_impuesto_id = target_tax_id
                else:
                    logger.warning(f"Target tax for condition {cond.nombre} not found.")
        
        await db.commit()
        logger.info("Seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed())
