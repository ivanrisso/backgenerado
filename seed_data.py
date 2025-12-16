
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoDoc, Iva
from sqlalchemy import select
from decimal import Decimal

async def seed_data():
    async with SessionLocal() as db:
        print("Seeding TipoDoc...")
        # Common AFIP Document Types
        tipo_docs = [
            {"id": 80, "tipo_doc_nombre": "CUIT", "codigo_arca": "80", "habilitado": True},
            {"id": 96, "tipo_doc_nombre": "DNI", "codigo_arca": "96", "habilitado": True},
            {"id": 86, "tipo_doc_nombre": "CUIL", "codigo_arca": "86", "habilitado": True},
            {"id": 87, "tipo_doc_nombre": "CDI", "codigo_arca": "87", "habilitado": True},
        ]

        for doc in tipo_docs:
            stmt = select(TipoDoc).where(TipoDoc.id == doc["id"])
            existing = (await db.execute(stmt)).scalar_one_or_none()
            if not existing:
                print(f"Creating TipoDoc: {doc['tipo_doc_nombre']}")
                new_doc = TipoDoc(**doc)
                db.add(new_doc)
            else:
                 print(f"TipoDoc {doc['tipo_doc_nombre']} already exists.")

        print("\nSeeding IVA...")
        # Common AFIP VAT Conditions
        ivas = [
            {"id": 1, "descripcion": "IVA Responsable Inscripto", "codigo": 1, "discriminado": True, "porcentaje": Decimal("21.00")},
            {"id": 4, "descripcion": "IVA Sujeto Exento", "codigo": 4, "discriminado": False, "porcentaje": Decimal("0.00")},
            {"id": 5, "descripcion": "Consumidor Final", "codigo": 5, "discriminado": False, "porcentaje": Decimal("0.00")},
            {"id": 6, "descripcion": "Responsable Monotributo", "codigo": 6, "discriminado": False, "porcentaje": Decimal("0.00")},
        ]

        for iva in ivas:
            stmt = select(Iva).where(Iva.id == iva["id"])
            existing = (await db.execute(stmt)).scalar_one_or_none()
            if not existing:
               print(f"Creating IVA: {iva['descripcion']}")
               new_iva = Iva(**iva)
               db.add(new_iva)
            else:
               print(f"IVA {iva['descripcion']} already exists.")

        await db.commit()
        print("\nSeeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
