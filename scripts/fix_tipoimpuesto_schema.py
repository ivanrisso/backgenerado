import asyncio
from sqlalchemy import text
from app.infrastructure.db.engine import SessionLocal

async def alter_table():
    async with SessionLocal() as session:
        # MySQL Syntax
        await session.execute(text("ALTER TABLE tipoimpuesto MODIFY nombre VARCHAR(50);"))
        await session.commit()
        print("Table altered successfully.")

if __name__ == "__main__":
    asyncio.run(alter_table())
