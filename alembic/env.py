import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1) Inserta el path raíz para que Python encuentre el paquete `app`
sys.path.insert(0, os.path.abspath(os.getcwd()))

# 2) Configura logging
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# 3) Importa Base desde orm_models.py
# 3) Importa Base desde orm_models.py
from app.infrastructure.db.orm_models import Base
from app.core.config import settings

target_metadata = Base.metadata

# Sobreescribir la URL de sqlalchemy con la de settings
# Alembic (sync) necesita un driver sincrónico.
if hasattr(settings, "ALEMBIC_URL") and settings.ALEMBIC_URL:
    db_url = settings.ALEMBIC_URL
else:
    # Fallback: intentar reemplazar aiomysql/asyncmy con pymysql
    db_url = settings.DATABASE_URL.replace("aiomysql", "pymysql").replace("asyncmy", "pymysql")

context.config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
