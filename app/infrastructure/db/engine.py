from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from pathlib import Path
import os

# Importa DeclarativeBase ya definida con tus modelos
from app.infrastructure.db.orm_models import Base

# Carga de variables de entorno
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# URL de la base de datos (aiomysql o equivalente)
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor asincrónico
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool
)

# Sesión asincrónica
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Crear tablas automáticamente al iniciar
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
