from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schemas import UsuarioCreate
from app.schemas.usuario import UsuarioResponse
from app.services.auth_service import AuthService
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.security.jwt_handler import decode_token
from typing import AsyncGenerator

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UsuarioCreate, db: AsyncSession = Depends(get_db_session)):
    auth_service = AuthService(db)
    return await auth_service.registrar_usuario(user_data)

@router.post("/login", summary="Login de usuario")
async def login_user(response: Response, form_data: UsuarioCreate, db: AsyncSession = Depends(get_db_session)):
    auth_service = AuthService(db)
    usuario = await auth_service.autenticar_usuario(email=form_data.usuario_email, password=form_data.usuario_password)
    access_token, refresh_token = auth_service.crear_tokens(usuario)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict", max_age=15*60)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Strict", max_age=7*24*60*60)
    return {"msg": "Inicio de sesión exitoso"}

@router.post("/refresh", summary="Renovación de sesión")
async def refresh_token(request: Request, response: Response, db: AsyncSession = Depends(get_db_session)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh no presente.")

    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido para refresco.")

    usuario_email = payload.get("sub")
    if not usuario_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sin subject válido.")

    auth_service = AuthService(db)
    usuario = await auth_service.usuario_repo.get_by_email(usuario_email)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    new_access, new_refresh = auth_service.crear_tokens(usuario)
    response.set_cookie(key="access_token", value=new_access, httponly=True, secure=True, samesite="Strict", max_age=15*60)
    response.set_cookie(key="refresh_token", value=new_refresh, httponly=True, secure=True, samesite="Strict", max_age=7*24*60*60)
    return {"msg": "Token renovado con éxito"}

@router.post("/logout", summary="Cerrar sesión")
async def logout_user(response: Response):
    """Borra cookies para cerrar sesión en el cliente."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"msg": "Sesión cerrada correctamente"}