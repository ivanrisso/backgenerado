#app/core/dependencies.py
# app/core/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.security.jwt_handler import decode_token
from app.repositories.usuario_repository import UsuarioRepositoryImpl
from app.infrastructure.db.orm_models import Usuario
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    payload = decode_token(token)
    email: str = payload.get("sub")

    if not email:
        raise credentials_exception

    usuario_repo = UsuarioRepositoryImpl(db)
    user = await usuario_repo.get_by_email(email)

    if user is None:
        raise credentials_exception

    return user

def require_roles(*allowed_roles: str):
    async def role_dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if not current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: el usuario no tiene roles asignados."
            )
        user_roles = [rol.rol_nombre.lower() for rol in current_user.roles]
        if not any(role.lower() in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requieren roles {allowed_roles}"
            )
        return current_user
    return role_dependency