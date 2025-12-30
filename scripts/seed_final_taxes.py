
import asyncio
import logging
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoImpuesto, CondicionTributaria
from app.domain.entities.enums import (
    TipoAplicacionEnum, BaseTributarioEnum, AmbitoImpuestoEnum, 
    CategoriaImpuestoEnum, TipoUsoImpuestoEnum, MetodoCalculoImpuestoEnum, 
    AmbitoUsoImpuestoEnum, CategoriaFiscalImpuestoEnum
)
from sqlalchemy import select, delete

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of IIBB Provinces from the image
PROVINCIAS_IIBB = [
    ("CABA", "Ciudad Autónoma de Buenos Aires"),
    ("PBA", "P. Buenos Aires"),
    ("C", "Catamarca"),
    ("CBA", "Córdoba"),
    ("CTS", "Corrientes"),
    ("ER", "Entre Ríos"),
    ("J", "Jujuy"),
    ("MZA", "Mendoza"),
    ("LR", "La Rioja"),
    ("S", "Salta"),
    ("SJ", "San Juan"),
    ("SL", "San Luis"),
    ("SF", "Santa Fe"),
    ("SE", "Santiago del Estero"),
    ("T", "Tucumán"),
    ("CHO", "Chaco"),
    ("CHT", "Chubut"),
    ("F", "Formosa"),
    ("MS", "Misiones"),
    ("N", "Neuquén"),
    ("LP", "La Pampa"),
    ("RN", "Río Negro"),
    ("SC", "Santa Cruz"),
    ("TF", "Tierra del Fuego"),
]

def get_base_iva_tax(nombre, rate, usage, active=True, codigo_afip=None, desc=None):
    return {
        "codigo_afip": codigo_afip or f"IVA_{rate}_{usage[0].upper()}",
        "nombre": nombre,
        "descripcion": desc or f"IVA {rate}%" if isinstance(rate, (int, float)) else desc or nombre,
        "tipo_aplicacion": TipoAplicacionEnum.SUMA,
        "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
        "ambito": AmbitoImpuestoEnum.NACIONAL,
        "categoria": CategoriaImpuestoEnum.IMPUESTO_DIRECTO,
        "porcentaje": rate if isinstance(rate, (int, float)) else 0.0,
        "tipo_uso": usage,
        "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
        "ambito_uso": AmbitoUsoImpuestoEnum.AMBOS,
        "importe": rate if isinstance(rate, (int, float)) else 0.0,
        "etiqueta_factura": nombre,
        "incluido_precio": False,
        "activo": active
    }

async def seed():
    async with SessionLocal() as db:
        logger.info("Starting final tax seeding...")

        # 1. Clean up existing taxes if any (as requested: "deja solo estos")
        # To be safe, we might want to just deactivate or delete if they are not used.
        # Here we will build the list first.
        
        target_taxes = []
        
        # Sequence 1: IVA 21%
        target_taxes.append(get_base_iva_tax("IVA 21%", 21.0, TipoUsoImpuestoEnum.VENTAS, codigo_afip="5"))
        target_taxes.append(get_base_iva_tax("IVA 21%", 21.0, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="5c"))

        # Sequence 2: Various IVAs
        target_taxes.append(get_base_iva_tax("IVA No Corresp", "no_corresp", TipoUsoImpuestoEnum.VENTAS, active=False, desc="IVA No Corresponde"))
        target_taxes.append(get_base_iva_tax("IVA No Corresp", "no_corresp", TipoUsoImpuestoEnum.COMPRAS, active=False, desc="IVA No Corresponde"))
        
        target_taxes.append(get_base_iva_tax("IVA No Grav", 0.0, TipoUsoImpuestoEnum.VENTAS, codigo_afip="2", desc="IVA No Gravado"))
        target_taxes.append(get_base_iva_tax("IVA No Grav", 0.0, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="2c", desc="IVA No Gravado"))
        
        target_taxes.append(get_base_iva_tax("IVA Exen", 0.0, TipoUsoImpuestoEnum.VENTAS, codigo_afip="1", desc="IVA Exento"))
        target_taxes.append(get_base_iva_tax("IVA Exen", 0.0, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="1c", desc="IVA Exento"))
        
        target_taxes.append(get_base_iva_tax("IVA 0%", 0.0, TipoUsoImpuestoEnum.VENTAS, codigo_afip="3"))
        target_taxes.append(get_base_iva_tax("IVA 0%", 0.0, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="3c"))
        
        target_taxes.append(get_base_iva_tax("IVA 10.5%", 10.5, TipoUsoImpuestoEnum.VENTAS, codigo_afip="4"))
        target_taxes.append(get_base_iva_tax("IVA 10.5%", 10.5, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="4c"))

        # Sequence 3: Others & 27%
        target_taxes.append({
            **get_base_iva_tax("Other taxes", 0.0, TipoUsoImpuestoEnum.COMPRAS, desc="Otros Impuestos"),
            "categoria": CategoriaImpuestoEnum.OTRO
        })
        target_taxes.append({
            **get_base_iva_tax("Internal taxes", 0.0, TipoUsoImpuestoEnum.COMPRAS, desc="Impuestos Internos"),
            "categoria": CategoriaImpuestoEnum.IMPUESTO_DIRECTO
        })
        target_taxes.append(get_base_iva_tax("IVA 27%", 27.0, TipoUsoImpuestoEnum.VENTAS, codigo_afip="6"))
        target_taxes.append(get_base_iva_tax("IVA 27%", 27.0, TipoUsoImpuestoEnum.COMPRAS, codigo_afip="6c"))

        # Sequence 4: IIBB Percepciones (Compras)
        for code, name in PROVINCIAS_IIBB:
            target_taxes.append({
                "codigo_afip": f"PIIBB_{code}_C",
                "nombre": f"P. IIBB {code}",
                "descripcion": f"Percepción IIBB {name}",
                "tipo_aplicacion": TipoAplicacionEnum.SUMA,
                "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
                "ambito": AmbitoImpuestoEnum.PROVINCIAL,
                "categoria": CategoriaImpuestoEnum.PERCEPCION,
                "porcentaje": 0.0,
                "tipo_uso": TipoUsoImpuestoEnum.COMPRAS,
                "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
                "ambito_uso": AmbitoUsoImpuestoEnum.AMBOS,
                "importe": 0.0,
                "etiqueta_factura": f"Perc IIBB {name}",
                "activo": True
            })
            
            # IIBB 0% for Ventas (FALSE)
            target_taxes.append({
                "codigo_afip": f"PIIBB_{code}_V",
                "nombre": f"P. IIBB {code} 0%",
                "descripcion": f"Percepción IIBB {name}",
                "tipo_aplicacion": TipoAplicacionEnum.SUMA,
                "base_calculo": BaseTributarioEnum.NETO_GRAVADO,
                "ambito": AmbitoImpuestoEnum.PROVINCIAL,
                "categoria": CategoriaImpuestoEnum.PERCEPCION,
                "porcentaje": 0.0,
                "tipo_uso": TipoUsoImpuestoEnum.VENTAS,
                "metodo_calculo": MetodoCalculoImpuestoEnum.PORCENTAJE,
                "ambito_uso": AmbitoUsoImpuestoEnum.AMBOS,
                "importe": 0.0,
                "etiqueta_factura": f"Perc IIBB {name}",
                "activo": False
            })

        # Perc IVA & Ganancias
        target_taxes.append({
            **get_base_iva_tax("Perc IVA", 0.0, TipoUsoImpuestoEnum.VENTAS, active=False, desc="Percepción IVA"),
            "categoria": CategoriaImpuestoEnum.PERCEPCION
        })
        target_taxes.append({
            **get_base_iva_tax("Perc Gananc", 0.0, TipoUsoImpuestoEnum.VENTAS, active=False, desc="Percepción Ganancias"),
            "categoria": CategoriaImpuestoEnum.PERCEPCION
        })
        target_taxes.append({
            **get_base_iva_tax("Perc Gananc", 0.0, TipoUsoImpuestoEnum.COMPRAS, active=True, desc="Percepción Ganancias"),
            "categoria": CategoriaImpuestoEnum.PERCEPCION
        })

        # Additional IVA
        target_taxes.append(get_base_iva_tax("IVA Adic 20%", 20.0, TipoUsoImpuestoEnum.COMPRAS, desc="IVA Adicional 20%"))

        # Sequence 9 & 10
        target_taxes.append(get_base_iva_tax("IVA 2.5", 2.5, TipoUsoImpuestoEnum.VENTAS, active=False))
        target_taxes.append(get_base_iva_tax("IVA 2.5", 2.5, TipoUsoImpuestoEnum.COMPRAS, active=False))
        target_taxes.append(get_base_iva_tax("IVA 5%", 5.0, TipoUsoImpuestoEnum.VENTAS, active=False))
        target_taxes.append(get_base_iva_tax("IVA 5%", 5.0, TipoUsoImpuestoEnum.COMPRAS, active=False))

        # EXECUTION
        # Delete all existing taxes to ensure ONLY these remain
        logger.info("Deleting existing taxes to fulfill 'leave only these' request...")
        await db.execute(delete(TipoImpuesto))
        await db.flush()

        logger.info(f"Creating {len(target_taxes)} taxes from reference image...")
        for tax_dict in target_taxes:
            db.add(TipoImpuesto(**tax_dict))
        
        await db.commit()
        logger.info("Tax creation completed. Re-associating conditions...")

        # 3. Re-associate Conditions
        # Re-get the new IVA 21% ID
        stmt = select(TipoImpuesto.id).where(TipoImpuesto.nombre == "IVA 21%", TipoImpuesto.tipo_uso == TipoUsoImpuestoEnum.VENTAS)
        res = await db.execute(stmt)
        iva_21_id = res.scalar_one_or_none()

        if iva_21_id:
            logger.info(f"Mapping all NACIONAL conditions to IVA 21% (ID: {iva_21_id})...")
            # Update all conditions that are Nacional
            from sqlalchemy import update
            from app.infrastructure.db.orm_models import CondicionTributaria as CondicionTributariaSQL
            
            stmt_update = (
                update(CondicionTributariaSQL)
                .where(CondicionTributariaSQL.ambito == AmbitoImpuestoEnum.NACIONAL)
                .values(tipo_impuesto_id=iva_21_id)
            )
            await db.execute(stmt_update)
            await db.commit()
            logger.info("Conditions associated to IVA 21%.")
        else:
            logger.warning("IVA 21% (Ventas) not found for re-association.")

        logger.info("Final tax synchronization completed successfully.")

if __name__ == "__main__":
    import sys
    # Fix for boolean False in script creation (was false lowercase)
    # Re-running the tool call with correct content.
    pass
