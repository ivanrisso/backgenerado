# app/infrastructure/db/engine.py

from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

# Tu Settings centralizado
from app.core.config import settings

# Tu metadata declarativa
from app.infrastructure.db.orm_models import Base

# URL de la base de datos desde settings
DATABASE_URL = settings.DATABASE_URL  # añade este campo en tu Settings

# Crea el engine asincrónico
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool
)

# Crea la fábrica de sesiones
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Función para crear tablas al iniciar
async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
