# ✅ app/repositories/localidad_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Localidad as LocalidadSQL
from app.domain.entities.localidad import Localidad
from app.domain.repository.localidad_repository_interfase import LocalidadRepositoryInterface
from app.domain.exceptions.localidad import LocalidadDuplicado, LocalidadInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class LocalidadRepositoryImpl(LocalidadRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, localidad_id: int) -> Optional[Localidad]:
        stmt = select(LocalidadSQL).where(LocalidadSQL.id == localidad_id)
        result = await self.db.execute(stmt)
        localidad_sql = result.scalar_one_or_none()
        return self._to_domain(localidad_sql) if localidad_sql else None

    async def get_all(self) -> List[Localidad]:
        stmt = select(LocalidadSQL)
        result = await self.db.execute(stmt)
        localidads_sql = result.scalars().all()
        return [self._to_domain(c) for c in localidads_sql]

    async def create(self, localidad: Localidad) -> Localidad:
        try:
            localidad_sql = self._to_orm(localidad)
            self.db.add(localidad_sql)
            await self.db.commit()
            await self.db.refresh(localidad_sql)
            return self._to_domain(localidad_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise LocalidadDuplicado("localidad_nombre o cod_postal", f"{localidad.localidad_nombre} / {localidad.cod_postal}")

                elif error_code == 1452:
                    if "provincia_id" in msg:
                        raise ClaveForaneaInvalida("provincia_id", str(localidad.provincia_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear localidad")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise LocalidadInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear localidad")

    async def update(self, localidad_id: int, localidad: Localidad) -> Optional[Localidad]:
        try:
            localidad_sql = await self.db.get(LocalidadSQL, localidad_id)
            if not localidad_sql:
                return None

            cambios = False
            for field, value in vars(localidad).items():
                if value is not None and hasattr(localidad_sql, field):
                    setattr(localidad_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(localidad_sql)

            return self._to_domain(localidad_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise LocalidadDuplicado("localidad_nombre o cod_postal", f"{localidad.localidad_nombre} / {localidad.cod_postal}")

                elif error_code == 1452:
                    if "provincia_id" in msg:
                        raise ClaveForaneaInvalida("provincia_id", str(localidad.provincia_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar localidad")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise LocalidadInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar localidad")


    async def delete(self, localidad_id: int) -> None:
        try:
            localidad_sql = await self.db.get(LocalidadSQL, localidad_id)
            if not localidad_sql:
                return

            await self.db.delete(localidad_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("localidad_id", str(localidad_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar localidad")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar localidad")


    def _to_domain(self, localidad_sql: LocalidadSQL) -> Localidad:
        return Localidad(
            id=localidad_sql.id,
            localidad_nombre=localidad_sql.localidad_nombre,
            cod_postal=localidad_sql.cod_postal,
            provincia_id=localidad_sql.provincia_id
        )


    def _to_orm(self, localidad: Localidad) -> LocalidadSQL:
        return LocalidadSQL(
            id=localidad.id,
            localidad_nombre=localidad.localidad_nombre,
            cod_postal=localidad.cod_postal,
            provincia_id=localidad.provincia_id
        )
