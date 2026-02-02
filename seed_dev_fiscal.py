import asyncio
from sqlalchemy import select
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoImpuesto, CondicionTributaria

# Minimal Dev Seed
SEEDS_TIPO_IMPUESTO = [
    {"codigo_afip": "30", "nombre": "IVA", "descripcion": "Impuesto al Valor Agregado", "tipo_aplicacion": "SUMA", "base_calculo": "SUBTOTAL", "categoria": "IMPUESTO_DIRECTO", "ambito": "NACIONAL", "tipo_uso": "VENTAS", "metodo_calculo": "PORCENTAJE", "ambito_uso": "AMBOS"},
    {"codigo_afip": "900", "nombre": "IIBB", "descripcion": "Ingresos Brutos", "tipo_aplicacion": "SUMA", "base_calculo": "SUBTOTAL", "categoria": "IMPUESTO_DIRECTO", "ambito": "PROVINCIAL", "tipo_uso": "VENTAS", "metodo_calculo": "PORCENTAJE", "ambito_uso": "AMBOS"},
]

SEEDS_CONDICION_TRIBUTARIA = [
    {"nombre": "Responsable Inscripto", "tipo_impuesto_cod": "30", "ambito": "NACIONAL"},
    {"nombre": "Monotributista", "tipo_impuesto_cod": "30", "ambito": "NACIONAL"},
    {"nombre": "Consumidor Final", "tipo_impuesto_cod": "30", "ambito": "NACIONAL"},
    {"nombre": "Exento", "tipo_impuesto_cod": "30", "ambito": "NACIONAL"},
    {"nombre": "IIBB Local", "tipo_impuesto_cod": "900", "ambito": "PROVINCIAL"},
]

async def seed():
    async with SessionLocal() as session:
        print("Seeding Fiscal Data...")
        
        # 1. Ensure TipoImpuesto
        for data in SEEDS_TIPO_IMPUESTO:
            stmt = select(TipoImpuesto).where(TipoImpuesto.codigo_afip == data["codigo_afip"])
            existing = (await session.execute(stmt)).scalar_one_or_none()
            
            if not existing:
                print(f"Creating TipoImpuesto: {data['nombre']}")
                new_ti = TipoImpuesto(**data)
                session.add(new_ti)
                await session.flush() # get ID
            else:
                print(f"TipoImpuesto {data['nombre']} exists.")
                # Update attributes to match ORM Enum Case Requirement just in case
                existing.categoria = data["categoria"]
                existing.ambito = data["ambito"]

        # Commit to save types
        await session.commit()
        
        # 2. Ensure CondicionTributaria
        for data in SEEDS_CONDICION_TRIBUTARIA:
            # Find Parent Type
            stmt_ti = select(TipoImpuesto).where(TipoImpuesto.codigo_afip == data["tipo_impuesto_cod"])
            parent = (await session.execute(stmt_ti)).scalar_one_or_none()
            
            if parent:
                # Check existence by Name + Type
                stmt = select(CondicionTributaria).where(
                    (CondicionTributaria.nombre == data["nombre"]) & 
                    (CondicionTributaria.tipo_impuesto_id == parent.id)
                )
                existing = (await session.execute(stmt)).scalar_one_or_none()
                
                if not existing:
                    print(f"Creating CondicionTributaria: {data['nombre']}")
                    new_ct = CondicionTributaria(
                        nombre=data["nombre"],
                        descripcion=data["nombre"],
                        ambito=data["ambito"],
                        tipo_impuesto_id=parent.id
                    )
                    session.add(new_ct)
                else:
                    print(f"CondicionTributaria {data['nombre']} exists.")
                    existing.ambito = data["ambito"] # formatting
            else:
                print(f"Parent Type {data['tipo_impuesto_cod']} not found for {data['nombre']}")

        await session.commit()
        print("Seeding Complete.")

if __name__ == "__main__":
    asyncio.run(seed())
