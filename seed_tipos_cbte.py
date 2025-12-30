
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoComprobante

async def seed_tipos():
    # AFIP Standard Codes
    tipos = [
        {"id": 1, "descripcion": "Factura A", "codigo_arca": "01"},
        {"id": 6, "descripcion": "Factura B", "codigo_arca": "06"},
        {"id": 11, "descripcion": "Factura C", "codigo_arca": "11"},
        {"id": 51, "descripcion": "Factura M", "codigo_arca": "51"},
        {"id": 3, "descripcion": "Nota de Credito A", "codigo_arca": "03"},
        {"id": 8, "descripcion": "Nota de Credito B", "codigo_arca": "08"},
        {"id": 13, "descripcion": "Nota de Credito C", "codigo_arca": "13"},
    ]

    async with SessionLocal() as session:
        for t in tipos:
            existing = await session.get(TipoComprobante, t["id"])
            if not existing:
                print(f"Creating {t['descripcion']}...")
                new_t = TipoComprobante(
                    id=t["id"],
                    descripcion=t["descripcion"],
                    codigo=t["codigo_arca"], # Assuming unique codigo mapped to arca
                    es_fiscal=True,
                    codigo_arca=t["codigo_arca"]
                )
                session.add(new_t)
            else:
                print(f"{t['descripcion']} already exists.")
                
        await session.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_tipos())
