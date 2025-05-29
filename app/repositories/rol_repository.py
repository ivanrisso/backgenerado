# ✅ app/repositories/rol_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import Rol as RolSQL
from app.domain.entities.rol import Rol
from app.domain.repository.rol_repository_interfase import RolRepositoryInterface
from app.domain.exceptions.rol import RolDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolRepositoryImpl(RolRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, rol_id: int) -> Optional[Rol]:
        stmt = select(RolSQL).where(RolSQL.id == rol_id)
        result = await self.db.execute(stmt)
        rol_sql = result.scalar_one_or_none()
        return self._to_domain(rol_sql) if rol_sql else None

    async def get_all(self) -> List[Rol]:
        stmt = select(RolSQL)
        result = await self.db.execute(stmt)
        rols_sql = result.scalars().all()
        return [self._to_domain(c) for c in rols_sql]

    async def create(self, rol: Rol) -> Rol:
        try:
            rol_sql = self._to_orm(rol)
            self.db.add(rol_sql)
            await self.db.commit()
            await self.db.refresh(rol_sql)
            return self._to_domain(rol_sql)
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rol")

    async def update(self, rol_id: int, rol: Rol) -> Optional[Rol]:
        try:
            rol_sql = await self.db.get(RolSQL, rol_id)
            if not rol_sql:
                return None

            cambios = False
            for field, value in vars(rol).items():
                if value is not None and hasattr(rol_sql, field):
                    setattr(rol_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(rol_sql)
                
            return self._to_domain(rol_sql)

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar rol")


    async def delete(self, rol_id: int) -> None:
        try:
            rol_sql = await self.db.get(RolSQL, rol_id)
            if not rol_sql:
                return

            await self.db.delete(rol_sql)
            await self.db.commit()
            
        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()
                if error_code == 1451:
                    # 1451 = Cannot delete or update a parent row: a foreign key constraint fails
                    raise ClaveForaneaInvalida("rol_id", str(rol_id))
            raise ErrorDeRepositorio("Error de integridad al eliminar rol")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rol")

    def _to_domain(self, rol_sql: RolSQL) -> Rol:
        return Rol(
            id=rol_sql.id,
            rol_nombre=rol_sql.rol_nombre,
            es_admin=rol_sql.es_admin
        )

    def _to_orm(self, rol: Rol) -> RolSQL:
        return RolSQL(
            id=rol.id,
            rol_nombre=rol.rol_nombre,
            es_admin=rol.es_admin
        )
