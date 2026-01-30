from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.usuario_repository import UsuarioRepositoryImpl
from app.schemas.auth_schemas import UsuarioCreate
from app.infrastructure.db.orm_models import Usuario
from app.infrastructure.security.password_hashing import hash_password, verify_password
from app.infrastructure.security.jwt_handler import create_access_token, create_refresh_token
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class AuthService:
    def __init__(self, db: AsyncSession):
        self.usuario_repo = UsuarioRepositoryImpl(db)

    async def registrar_usuario(self, data: UsuarioCreate) -> Usuario:
        usuario_existente = await self.usuario_repo.get_by_email(data.usuario_email)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        usuario_nuevo = Usuario(
            usuario_email=data.usuario_email,
            usuario_password=hash_password(data.usuario_password),
            nombre=data.nombre,
            apellido=data.apellido
        )
        return await self.usuario_repo.create(usuario_nuevo)

    async def autenticar_usuario(self, email: str, password: str) -> Usuario:
        
        logger.info(f"Intento de login para: {email}")
        
        # Buscar usuario
        usuario = await self.usuario_repo.get_by_email(email)
        
        if not usuario:
            logger.warning(f"Login fallido: Usuario {email} no encontrado.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas (Usuario no existe).",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        if not verify_password(password, usuario.usuario_password):
            logger.warning(f"Login fallido: Password incorrecto para {email}.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas (Password incorrecto).",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        return usuario

    def crear_tokens(self, usuario: Usuario) -> tuple[str, str]:
        user_data = {"sub": usuario.usuario_email, "type": "access"}
        access_token = create_access_token(user_data)
        refresh_data = {"sub": usuario.usuario_email, "type": "refresh"}
        refresh_token = create_refresh_token(refresh_data)
        return access_token, refresh_token
