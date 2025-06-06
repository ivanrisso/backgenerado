# ✅ app/repositories/usuario_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.infrastructure.db.orm_models import Usuario as UsuarioSQL
from app.domain.entities.usuario import Usuario
from app.domain.entities.rol import Rol
from app.domain.repository.usuario_repository_interfase import UsuarioRepositoryInterface
from app.domain.exceptions.usuario import UsuarioDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

class UsuarioRepositoryImpl(UsuarioRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        stmt = select(UsuarioSQL).where(UsuarioSQL.id == usuario_id)
        result = await self.db.execute(stmt)
        usuario_sql = result.scalar_one_or_none()
        return self._to_domain(usuario_sql) if usuario_sql else None

    async def get_by_email(self, usuario_mail: str) -> Optional[Usuario]:
        #stmt = select(UsuarioSQL).where(UsuarioSQL.usuario_email == usuario_mail)        
        stmt = (select(UsuarioSQL).options(selectinload(UsuarioSQL.roles)).where(UsuarioSQL.usuario_email == usuario_mail))
        result = await self.db.execute(stmt)
        usuario_sql = result.scalar_one_or_none()                
        return self._to_domain(usuario_sql) if usuario_sql else None

    async def get_all(self) -> List[Usuario]:
        stmt = select(UsuarioSQL)
        result = await self.db.execute(stmt)
        usuarios_sql = result.scalars().all()
        return [self._to_domain(c) for c in usuarios_sql]

    async def create(self, usuario: Usuario) -> Usuario:
        try:
            usuario_sql = self._to_orm(usuario)
            self.db.add(usuario_sql)
            await self.db.commit()
            await self.db.refresh(usuario_sql)
            
            stmt = (
                select(UsuarioSQL)
                .options(selectinload(UsuarioSQL.roles))
                .where(UsuarioSQL.id == usuario_sql.id)
            )
            result = await self.db.execute(stmt)
            usuario_sql = result.scalar_one()
            
            return self._to_domain(usuario_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "usuario_mail" in msg:
                        raise UsuarioDuplicado("mail", usuario.usuario_email)
                    elif "primary" in msg:
                        raise UsuarioDuplicado("id", str(usuario.id))
                    else:
                        raise UsuarioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear usuario")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as ex:
            logger.error(f"❌ Error SQLAlchemy al crear usuariooooooooooo: {ex}")
            raise ErrorDeRepositorio("Error inesperado al crear usuario")

    async def update(self, usuario_id: int, usuario: Usuario) -> Optional[Usuario]:
        try:
            usuario_sql = await self.db.get(UsuarioSQL, usuario_id)
            if not usuario_sql:
                return None

            cambios = False
            for field, value in vars(usuario).items():
                if value is not None and hasattr(usuario_sql, field):
                    setattr(usuario_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(usuario_sql)
                
            stmt = (
                select(UsuarioSQL)
                .options(selectinload(UsuarioSQL.roles))
                .where(UsuarioSQL.id == usuario_sql.id)
            )
            result = await self.db.execute(stmt)
            usuario_sql = result.scalar_one()
                            
            return self._to_domain(usuario_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "usuario_mail" in msg:
                        raise UsuarioDuplicado("mail", usuario.usuario_email)
                    elif "primary" in msg:
                        raise UsuarioDuplicado("id", str(usuario.id))
                    else:
                        raise UsuarioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar usuario")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            logger.info("acaaaaaa")
            raise ErrorDeRepositorio("Error inesperado al actualizar usuario")


    async def delete(self, usuario_id: int) -> None:
        try:
            usuario_sql = await self.db.get(UsuarioSQL, usuario_id)
            if not usuario_sql:
                return

            await self.db.delete(usuario_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("usuario_id", str(usuario_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar usuario")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar usuario")

    def _to_domain(self, usuario_sql: UsuarioSQL) -> Usuario:
        return Usuario(
            id=usuario_sql.id,
            usuario_email=usuario_sql.usuario_email,
            usuario_password=usuario_sql.usuario_password,
            nombre=usuario_sql.nombre,
            apellido=usuario_sql.apellido,
            roles = [
            Rol(
                id=rol.id,
                rol_nombre=rol.rol_nombre,
                es_admin=rol.es_admin
            ) for rol in usuario_sql.roles
            ] if usuario_sql.roles else []

        )
    
    def _to_orm(self, usuario: Usuario) -> UsuarioSQL:
        return UsuarioSQL(
            id=usuario.id,
            usuario_email=usuario.usuario_email,
            usuario_password=usuario.usuario_password, #ya debe venir hasheado
            nombre=usuario.nombre,
            apellido=usuario.apellido
        )
        
        
        