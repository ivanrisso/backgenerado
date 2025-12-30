
import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import engine, Base
from app.infrastructure.db.orm_models import Imputacion

async def migrate():
    async with engine.begin() as conn:
        # 1. Add 'saldo' column to 'comprobante' table if not exists
        try:
            # Check if column exists (MySQL specific)
            # Or just try to add it and ignore error? Safer to check?
            # Simple approach: Try ADD COLUMN.
            await conn.execute(text("ALTER TABLE comprobante ADD COLUMN saldo FLOAT NOT NULL DEFAULT 0.0"))
            print("Columna 'saldo' agregada a tabla comprobante.")
            
            # Initialize saldo = total for all existing invoices
            await conn.execute(text("UPDATE comprobante SET saldo = total"))
            print("Saldos inicializados igual al total.")
            
        except Exception as e:
            print(f"Columna saldo ya existe o error: {e}")

        # 2. Create 'imputacion' table
        # We can use create_all logic only for new tables
        await conn.run_sync(Base.metadata.create_all)
        print("Tablas nuevas (imputacion) creadas si no existían.")

if __name__ == "__main__":
    asyncio.run(migrate())
