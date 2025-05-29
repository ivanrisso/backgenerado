# ✅ app/repositories/provincia_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import Provincia as ProvinciaSQL
from app.domain.entities.provincia import Provincia
from app.domain.repository.provincia_repository_interfase import ProvinciaRepositoryInterface
from app.domain.exceptions.provincia import ProvinciaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ProvinciaRepositoryImpl(ProvinciaRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, provincia_id: int) -> Optional[Provincia]:
        stmt = select(ProvinciaSQL).where(ProvinciaSQL.id == provincia_id)
        result = await self.db.execute(stmt)
        provincia_sql = result.scalar_one_or_none()
        return self._to_domain(provincia_sql) if provincia_sql else None

    async def get_all(self) -> List[Provincia]:
        stmt = select(ProvinciaSQL)
        result = await self.db.execute(stmt)
        provincias_sql = result.scalars().all()
        return [self._to_domain(c) for c in provincias_sql]

    async def create(self, provincia: Provincia) -> Provincia:
        try:
            provincia_sql = self._to_orm(provincia)
            self.db.add(provincia_sql)
            await self.db.commit()
            await self.db.refresh(provincia_sql)
            return self._to_domain(provincia_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "provincia_nombre" in msg:
                        raise ProvinciaDuplicado("provincia_nombre", provincia.provincia_nombre)
                    elif "primary" in msg:
                        raise ProvinciaDuplicado("id", str(provincia.id))
                    else:
                        raise ProvinciaDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "pais_id" in msg:
                        raise ClaveForaneaInvalida("pais_id", str(provincia.pais_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear provincia")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear provincia")

    async def update(self, provincia_id: int, provincia: Provincia) -> Optional[Provincia]:
        try:
            provincia_sql = await self.db.get(ProvinciaSQL, provincia_id)
            if not provincia_sql:
                return None

            cambios = False
            for field, value in vars(provincia).items():
                if value is not None and hasattr(provincia_sql, field):
                    setattr(provincia_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(provincia_sql)

            return self._to_domain(provincia_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "provincia_nombre" in msg:
                        raise ProvinciaDuplicado("provincia_nombre", provincia.provincia_nombre)
                    elif "primary" in msg:
                        raise ProvinciaDuplicado("id", str(provincia.id))
                    else:
                        raise ProvinciaDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "pais_id" in msg:
                        raise ClaveForaneaInvalida("pais_id", str(provincia.pais_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar provincia")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar provincia")


    async def delete(self, provincia_id: int) -> None:
        try:
            provincia_sql = await self.db.get(ProvinciaSQL, provincia_id)
            if not provincia_sql:
                return

            await self.db.delete(provincia_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    # Relación con localidad u otro modelo
                    raise ClaveForaneaInvalida("provincia_id", str(provincia_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar provincia")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar provincia")


    def _to_domain(self, provincia_sql: ProvinciaSQL) -> Provincia:
        return Provincia(
            id=provincia_sql.id,
            provincia_nombre=provincia_sql.provincia_nombre,
            pais_id=provincia_sql.pais_id
        )

    def _to_orm(self, provincia: Provincia) -> ProvinciaSQL:
        return ProvinciaSQL(
            id=provincia.id,
            provincia_nombre=provincia.provincia_nombre,
            pais_id=provincia.pais_id
        )
