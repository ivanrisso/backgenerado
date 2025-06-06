# ✅ app/repositories/rolesusuario_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import RolesUsuario as RolesUsuarioSQL
from app.domain.entities.rolesusuario import RolesUsuario
from app.domain.repository.rolesusuario_repository_interfase import RolesUsuarioRepositoryInterface
from app.domain.exceptions.rolesusuario import RolesUsuarioDuplicado, RolesUsuarioInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolesUsuarioRepositoryImpl(RolesUsuarioRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, rolesusuario_id: int) -> Optional[RolesUsuario]:
        stmt = select(RolesUsuarioSQL).where(RolesUsuarioSQL.id == rolesusuario_id)
        result = await self.db.execute(stmt)
        rolesusuario_sql = result.scalar_one_or_none()
        return self._to_domain(rolesusuario_sql) if rolesusuario_sql else None

    async def get_by_usuario_id(self, value) -> Optional[RolesUsuario]:
        stmt = select(RolesUsuarioSQL).where(RolesUsuarioSQL.usuario_id == value)
        result = await self.db.execute(stmt)
        rolesusuario_sql = result.scalar_one_or_none()
        return self._to_domain(rolesusuario_sql) if rolesusuario_sql else None

    async def get_all(self) -> List[RolesUsuario]:
        stmt = select(RolesUsuarioSQL)
        result = await self.db.execute(stmt)
        rolesusuarios_sql = result.scalars().all()
        return [self._to_domain(c) for c in rolesusuarios_sql]

    async def create(self, rolesusuario: RolesUsuario) -> RolesUsuario:
        try:
            rolesusuario_sql = self._to_orm(rolesusuario)
            self.db.add(rolesusuario_sql)
            await self.db.commit()
            await self.db.refresh(rolesusuario_sql)
            return self._to_domain(rolesusuario_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                logger.error(f"Integritt Error: {msg}")

                if error_code == 1062:
                    if "primary" in msg:
                        raise RolesUsuarioDuplicado("id", str(rolesusuario.id))
                    else:
                        raise RolesUsuarioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "usuario_id" in msg:
                        raise ClaveForaneaInvalida("usuario_id", str(rolesusuario.usuario_id))
                    elif "rol_id" in msg:
                        raise ClaveForaneaInvalida("rol_id", str(rolesusuario.rol_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear rolesusuario")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise RolesUsuarioInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rolesusuario")

    async def update(self, rolesusuario_id: int, rolesusuario: RolesUsuario) -> Optional[RolesUsuario]:
        try:
            rolesusuario_sql = await self.db.get(RolesUsuarioSQL, rolesusuario_id)
            if not rolesusuario_sql:
                return None

            cambios = False
            for field, value in vars(rolesusuario).items():
                if value is not None and hasattr(rolesusuario_sql, field):
                    setattr(rolesusuario_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(rolesusuario_sql)
                
            return self._to_domain(rolesusuario_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise RolesUsuarioDuplicado("id", str(rolesusuario.id))
                    else:
                        raise RolesUsuarioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "usuario_id" in msg:
                        raise ClaveForaneaInvalida("usuario_id", str(rolesusuario.usuario_id))
                    elif "rol_id" in msg:
                        raise ClaveForaneaInvalida("rol_id", str(rolesusuario.rol_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar rolesusuario")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise RolesUsuarioInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar rolesusuario")


    async def delete(self, rolesusuario_id: int) -> None:
        try:
            rolesusuario_sql = await self.db.get(RolesUsuarioSQL, rolesusuario_id)
            if not rolesusuario_sql:
                return

            await self.db.delete(rolesusuario_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("rolesusuario_id", str(rolesusuario_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar rolesusuario")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rolesusuario")

    def _to_domain(self, rolesusuario_sql: RolesUsuarioSQL) -> RolesUsuario:
        return RolesUsuario(
            usuario_id=rolesusuario_sql.usuario_id,
            rol_id=rolesusuario_sql.rol_id
        )

    def _to_orm(self, rolesusuario: RolesUsuario) -> RolesUsuarioSQL:
        return RolesUsuarioSQL(
            usuario_id=rolesusuario.usuario_id,
            rol_id=rolesusuario.rol_id
        )




