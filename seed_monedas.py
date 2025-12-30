
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Moneda

async def seed_monedas():
    monedas = [
        {"id": 1, "descripcion": "Pesos Argentinos", "codigo": "PES", "codigo_arca": "PES"},
        {"id": 2, "descripcion": "Dolar Estadounidense", "codigo": "DOL", "codigo_arca": "DOL"},
    ]

    async with SessionLocal() as session:
        for m in monedas:
            existing = await session.get(Moneda, m["id"])
            if not existing:
                print(f"Creating {m['descripcion']}...")
                new_m = Moneda(
                    id=m["id"],
                    descripcion=m["descripcion"],
                    codigo=m["codigo"],
                    codigo_arca=m["codigo_arca"]
                )
                session.add(new_m)
            else:
                print(f"Updating {m['descripcion']}...")
                existing.descripcion = m["descripcion"]
                existing.codigo = m["codigo"]
                existing.codigo_arca = m["codigo_arca"]
        
        await session.commit()
        print("Monedas seeded.")

if __name__ == "__main__":
    asyncio.run(seed_monedas())
