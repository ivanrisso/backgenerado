
import asyncio
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import TipoComprobante
from sqlalchemy import select

async def check_tipos():
    async with SessionLocal() as session:
        result = await session.execute(select(TipoComprobante))
        tipos = result.scalars().all()
        print(f"{'ID':<5} | {'DESCRIPCION':<25} | {'CODIGO ARCA':<10} | {'LETRA':<5}")
        print("-" * 55)
        for t in tipos:
            # Assuming 'letra' might be a field? If not, we guess by desc
            print(f"{t.id:<5} | {t.descripcion:<25} | {t.codigo_arca:<10} | {getattr(t, 'letra', '?'):<5}")

if __name__ == "__main__":
    asyncio.run(check_tipos())
