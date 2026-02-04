from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.infrastructure.db.engine import create_db_and_tables
from app.routes import include_all_routes
from app.core.middleware import ExceptionHandlingMiddleware
from app.core.logger import init_logger
import logging

init_logger()
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Creando base de datos y DB")
    await create_db_and_tables()
    yield

app = FastAPI(title="Billing Backend System", lifespan=lifespan)

# Middleware global de errores
app.add_middleware(ExceptionHandlingMiddleware)

from app.core.config import settings

# CORS settings (pueden ajustarse para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar si no existen


# Registrar todas las rutas
include_all_routes(app)

# Endpoint de prueba
@app.get("/ping")
def ping():
    return {"message": "pong"}
