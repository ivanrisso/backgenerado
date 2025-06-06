# ✅ app/repositories/tipotel_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import TipoTel as TipoTelSQL
from app.domain.entities.tipotel import TipoTel
from app.domain.repository.tipotel_repository_interfase import TipoTelRepositoryInterface
from app.domain.exceptions.tipotel import TipoTelDuplicado, TipoTelInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoTelRepositoryImpl(TipoTelRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipotel_id: int) -> Optional[TipoTel]:
        stmt = select(TipoTelSQL).where(TipoTelSQL.id == tipotel_id)
        result = await self.db.execute(stmt)
        tipotel_sql = result.scalar_one_or_none()
        return self._to_domain(tipotel_sql) if tipotel_sql else None

    async def get_all(self) -> List[TipoTel]:
        stmt = select(TipoTelSQL)
        result = await self.db.execute(stmt)
        tipotels_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipotels_sql]

    async def create(self, tipotel: TipoTel) -> TipoTel:
        try:
            tipotel_sql = self._to_orm(tipotel)
            self.db.add(tipotel_sql)
            await self.db.commit()
            await self.db.refresh(tipotel_sql)
            return self._to_domain(tipotel_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoTelDuplicado("id", str(tipotel.id))
                    else:
                        raise TipoTelDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear tipotel")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TipoTelInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipotel")

    async def update(self, tipotel_id: int, tipotel: TipoTel) -> Optional[TipoTel]:
        try:
            tipotel_sql = await self.db.get(TipoTelSQL, tipotel_id)
            if not tipotel_sql:
                return None

            cambios = False
            for field, value in vars(tipotel).items():
                if value is not None and hasattr(tipotel_sql, field):
                    setattr(tipotel_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(tipotel_sql)
                
            return self._to_domain(tipotel_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoTelDuplicado("id", str(tipotel.id))
                    else:
                        raise TipoTelDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar tipotel")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TipoTelInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipotel")


    async def delete(self, tipotel_id: int) -> None:
        try:
            tipotel_sql = await self.db.get(TipoTelSQL, tipotel_id)
            if not tipotel_sql:
                return

            await self.db.delete(tipotel_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("tipotel_id", str(tipotel_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar tipotel")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipotel")

    def _to_domain(self, tipotel_sql: TipoTelSQL) -> TipoTel:
        return TipoTel(
            id=tipotel_sql.id,
            nombre=tipotel_sql.nombre
        )

    def _to_orm(self, tipotel: TipoTel) -> TipoTelSQL:
        return TipoTelSQL(
            id=tipotel.id,
            nombre=tipotel.nombre
        )
