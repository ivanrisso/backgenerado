
import asyncio
from app.infrastructure.db.engine import SessionLocal
from sqlalchemy import text
from app.infrastructure.db.orm_models import Iva

async def fix_and_seed():
    async with SessionLocal() as session:
        # 1. Drop Index
        try:
            print("Dropping UNIQUE constraint on iva.codigo...")
            await session.execute(text("DROP INDEX ix_iva_codigo ON iva"))
            await session.commit()
            print("Constraint dropped.")
        except Exception as e:
            print(f"Index drop failed (maybe already dropped?): {e}")

        # 2. Seed Rates
        rates = [
            {"id": 21, "descripcion": "IVA 21%", "codigo": 5, "porcentaje": 21.0},
            {"id": 10, "descripcion": "IVA 10.5%", "codigo": 4, "porcentaje": 10.5},
            {"id": 27, "descripcion": "IVA 27%", "codigo": 6, "porcentaje": 27.0},
            {"id": 30, "descripcion": "IVA 0%", "codigo": 3, "porcentaje": 0.0},
            {"id": 50, "descripcion": "IVA 5%", "codigo": 8, "porcentaje": 5.0},
            {"id": 25, "descripcion": "IVA 2.5%", "codigo": 9, "porcentaje": 2.5},
        ]
        
        for r in rates:
            existing = await session.get(Iva, r["id"])
            if not existing:
                print(f"Creating {r['descripcion']}...")
                new_iva = Iva(
                    id=r["id"],
                    descripcion=r["descripcion"],
                    codigo=r["codigo"],
                    porcentaje=r["porcentaje"],
                    discriminado=True
                )
                session.add(new_iva)
            else:
                 print(f"Updating {r['descripcion']}...")
                 existing.descripcion = r["descripcion"]
                 existing.codigo = r["codigo"]
                 existing.porcentaje = r["porcentaje"]
        
        await session.commit()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(fix_and_seed())
