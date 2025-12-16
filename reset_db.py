import asyncio
from app.infrastructure.db.engine import engine
from app.infrastructure.db.orm_models import Base

async def reset_db():
    async with engine.begin() as conn:
        print("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database reset complete.")

if __name__ == "__main__":
    asyncio.run(reset_db())
