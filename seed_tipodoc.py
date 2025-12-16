import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoDoc
from sqlalchemy import select

async def main():
    async with SessionLocal() as db:
        # Check if exists
        stmt = select(TipoDoc)
        result = await db.execute(stmt)
        if result.scalars().first():
            print("TipoDoc already seeded")
            return

        types = [
            TipoDoc(id=80, tipo_doc_nombre="CUIT", codigo_arca="80", habilitado=True),
            TipoDoc(id=86, tipo_doc_nombre="CUIL", codigo_arca="86", habilitado=True),
            TipoDoc(id=96, tipo_doc_nombre="DNI", codigo_arca="96", habilitado=True),
            TipoDoc(id=99, tipo_doc_nombre="Sin Identificar", codigo_arca="99", habilitado=True),
        ]
        db.add_all(types)
        await db.commit()
        print("Seeded TipoDoc")

if __name__ == "__main__":
    asyncio.run(main())
