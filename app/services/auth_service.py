from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth_schemas import UsuarioCreate
from app.infrastructure.db.orm_models import Usuario
from app.infrastructure.security.password_hashing import hash_password, verify_password
from app.infrastructure.security.jwt_handler import create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.usuario_repo = UsuarioRepository(db)

    async def registrar_usuario(self, data: UsuarioCreate) -> Usuario:
        """
        Registra un nuevo usuario en el sistema.
        Verifica que el correo electrónico no esté previamente registrado.
        """
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

    async def autenticar_usuario(self, email: str, password: str) -> str:
        """
        Verifica las credenciales del usuario y devuelve un token JWT si son válidas.
        """
        usuario = await self.usuario_repo.get_by_email(email)

        if not usuario or not verify_password(password, usuario.usuario_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Se puede agregar rol u otros claims si lo deseas
        token = create_access_token({ "sub": usuario.usuario_email })
        return token
