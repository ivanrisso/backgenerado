import asyncio
from app.infrastructure.db.engine import SessionLocal
from sqlalchemy import select
from app.infrastructure.db.orm_models import TipoDoc, Iva

async def check_params():
    async with SessionLocal() as db:
        print("--- TipoDoc ---")
        stmt = select(TipoDoc)
        docs = (await db.execute(stmt)).scalars().all()
        for d in docs:
            print(f"ID: {d.id}, Nombre: {d.tipo_doc_nombre}, Codigo: {d.codigo_arca}")
        
        print("\n--- IVA ---")
        stmt = select(Iva)
        ivas = (await db.execute(stmt)).scalars().all()
        for i in ivas:
            print(f"ID: {i.id}, Descripcion: {i.descripcion}, Codigo: {i.codigo}")

if __name__ == "__main__":
    asyncio.run(check_params())
