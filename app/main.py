from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.infrastructure.db.engine import create_db_and_tables
from app.routes import include_all_routes
from app.core.middleware import ExceptionHandlingMiddleware
import logging

# Configurar logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(title="Billing Backend System")

# Middleware global de errores
app.add_middleware(ExceptionHandlingMiddleware)

# CORS settings (pueden ajustarse para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar si no existen
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# Registrar todas las rutas
include_all_routes(app)

# Endpoint de prueba
@app.get("/ping")
def ping():
    return {"message": "pong"}
