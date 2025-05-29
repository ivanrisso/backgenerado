# ✅ app/repositories/moneda_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import Moneda as MonedaSQL
from app.domain.entities.moneda import Moneda
from app.domain.repository.moneda_repository_interfase import MonedaRepositoryInterface
from app.domain.exceptions.moneda import MonedaDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MonedaRepositoryImpl(MonedaRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, moneda_id: int) -> Optional[Moneda]:
        stmt = select(MonedaSQL).where(MonedaSQL.id == moneda_id)
        result = await self.db.execute(stmt)
        moneda_sql = result.scalar_one_or_none()
        return self._to_domain(moneda_sql) if moneda_sql else None

    async def get_all(self) -> List[Moneda]:
        stmt = select(MonedaSQL)
        result = await self.db.execute(stmt)
        monedas_sql = result.scalars().all()
        return [self._to_domain(c) for c in monedas_sql]

    async def create(self, moneda: Moneda) -> Moneda:
        try:
            moneda_sql = self._to_orm(moneda)
            self.db.add(moneda_sql)
            await self.db.commit()
            await self.db.refresh(moneda_sql)
            return self._to_domain(moneda_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise MonedaDuplicado("codigo", moneda.codigo)
                    elif "primary" in msg:
                        raise MonedaDuplicado("id", str(moneda.id))
                    else:
                        raise MonedaDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al crear moneda")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear moneda")


    async def update(self, moneda_id: int, moneda: Moneda) -> Optional[Moneda]:
        try:
            moneda_sql = await self.db.get(MonedaSQL, moneda_id)
            if not moneda_sql:
                return None

            cambios = False
            for field, value in vars(moneda).items():
                if value is not None and hasattr(moneda_sql, field):
                    setattr(moneda_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(moneda_sql)

            return self._to_domain(moneda_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise MonedaDuplicado("codigo", moneda.codigo)
                    elif "primary" in msg:
                        raise MonedaDuplicado("id", str(moneda.id))
                    else:
                        raise MonedaDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al actualizar moneda")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar moneda")


    async def delete(self, moneda_id: int) -> None:
        try:
            moneda_sql = await self.db.get(MonedaSQL, moneda_id)
            if not moneda_sql:
                return

            await self.db.delete(moneda_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("moneda_id", str(moneda_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar moneda")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar moneda")

    def _to_domain(self, moneda_sql: MonedaSQL) -> Moneda:
        return Moneda(
            id=moneda_sql.id,
            codigo=moneda_sql.codigo,
            descripcion=moneda_sql.descripcion
        )

    def _to_orm(self, moneda: Moneda) -> MonedaSQL:
        return MonedaSQL(
            id=moneda.id,
            codigo=moneda.codigo,
            descripcion=moneda.descripcion
        )
