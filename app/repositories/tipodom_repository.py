# ✅ app/repositories/tipodom_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import TipoDom as TipoDomSQL
from app.domain.entities.tipodom import TipoDom
from app.domain.repository.tipodom_repository_interfase import TipoDomRepositoryInterface
from app.domain.exceptions.tipodom import TipoDomDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoDomRepositoryImpl(TipoDomRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipodom_id: int) -> Optional[TipoDom]:
        stmt = select(TipoDomSQL).where(TipoDomSQL.id == tipodom_id)
        result = await self.db.execute(stmt)
        tipodom_sql = result.scalar_one_or_none()
        return self._to_domain(tipodom_sql) if tipodom_sql else None

    async def get_all(self) -> List[TipoDom]:
        stmt = select(TipoDomSQL)
        result = await self.db.execute(stmt)
        tipodoms_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipodoms_sql]

    async def create(self, tipodom: TipoDom) -> TipoDom:
        try:
            tipodom_sql = self._to_orm(tipodom)
            self.db.add(tipodom_sql)
            await self.db.commit()
            await self.db.refresh(tipodom_sql)
            return self._to_domain(tipodom_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                logger.error(f"Integritt Error: {msg}")

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoDomDuplicado("id", str(tipodom.id))
                    else:
                        raise TipoDomDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear tipodom")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipodom")

    async def update(self, tipodom_id: int, tipodom: TipoDom) -> Optional[TipoDom]:
        try:
            tipodom_sql = await self.db.get(TipoDomSQL, tipodom_id)
            if not tipodom_sql:
                return None

            cambios = False
            for field, value in vars(tipodom).items():
                if value is not None and hasattr(tipodom_sql, field):
                    setattr(tipodom_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(tipodom_sql)
                
            return self._to_domain(tipodom_sql)

        except IntegrityError as e:
            
            logger.info("acaaaaaa1111")
            
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoDomDuplicado("id", str(tipodom.id))
                    else:
                        raise TipoDomDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar tipodom")

        except OperationalError:
            logger.info("acaaaaaa33333")
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            logger.info("acaaaaaa")
            raise ErrorDeRepositorio("Error inesperado al actualizar tipodom")


    async def delete(self, tipodom_id: int) -> None:
        try:
            tipodom_sql = await self.db.get(TipoDomSQL, tipodom_id)
            if not tipodom_sql:
                return

            await self.db.delete(tipodom_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("tipodom_id", str(tipodom_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar tipodom")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipodom")

    def _to_domain(self, tipodom_sql: TipoDomSQL) -> TipoDom:
        return TipoDom(
            id=tipodom_sql.id,
            nombre=tipodom_sql.nombre
        )

    def _to_orm(self, tipodom: TipoDom) -> TipoDomSQL:
        return TipoDomSQL(
            id=tipodom.id,
            nombre=tipodom.nombre
        )
