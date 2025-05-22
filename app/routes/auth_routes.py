from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schemas import UsuarioCreate, TokenResponse
from app.schemas.usuario import UsuarioResponse
from app.services.auth_service import AuthService
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.db.orm_models import Usuario
from typing import AsyncGenerator


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# Dependency: Session de base de datos asincrónica
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de nuevo usuario",
    response_description="Usuario registrado exitosamente"
)


async def register_user(
    user_data: UsuarioCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Registra un nuevo usuario con validación de email único y contraseña encriptada."""
    auth_service = AuthService(db)
    return await auth_service.registrar_usuario(user_data)

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login de usuario",
    response_description="Token JWT generado"
)


async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """Autentica al usuario y devuelve un token JWT si las credenciales son válidas."""
    auth_service = AuthService(db)
    token = await auth_service.autenticar_usuario(
        email=form_data.username,
        password=form_data.password
    )
    return TokenResponse(access_token=token)
