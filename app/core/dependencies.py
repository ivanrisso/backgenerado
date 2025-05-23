from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.infrastructure.security.jwt_handler import decode_access_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models import Usuario
from typing import AsyncGenerator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    email: str = payload.get("sub")

    if not email:
        raise credentials_exception

    usuario_repo = UsuarioRepository(db)
    user = await usuario_repo.get_by_email(email)

    if user is None:
        raise credentials_exception

    return user

def require_roles(*allowed_roles: str):
    async def role_dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if not current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: el usuario no tiene roles asignados.",
            )
        user_roles = [rol.rol_nombre.lower() for rol in current_user.roles]
        if not any(role.lower() in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: se requieren roles {allowed_roles}",
            )
        return current_user
    return role_dependency
