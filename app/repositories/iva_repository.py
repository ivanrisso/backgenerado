# ✅ app/repositories/iva_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError

from typing import Optional, List

from app.infrastructure.db.orm_models import Iva as IvaSQL
from app.domain.entities.iva import Iva
from app.domain.repository.iva_repository_interfase import IvaRepositoryInterface
from app.domain.exceptions.iva import IvaDuplicado, IvaInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class IvaRepositoryImpl(IvaRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, iva_id: int) -> Optional[Iva]:
        stmt = select(IvaSQL).where(IvaSQL.id == iva_id)
        result = await self.db.execute(stmt)
        iva_sql = result.scalar_one_or_none()
        return self._to_domain(iva_sql) if iva_sql else None

    async def get_all(self) -> List[Iva]:
        stmt = select(IvaSQL)
        result = await self.db.execute(stmt)
        ivas_sql = result.scalars().all()
        return [self._to_domain(c) for c in ivas_sql]

    async def create(self, iva: Iva) -> Iva:
        try:
            iva_sql = self._to_orm(iva)
            self.db.add(iva_sql)
            await self.db.commit()
            await self.db.refresh(iva_sql)
            return self._to_domain(iva_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise IvaDuplicado("codigo", str(iva.codigo))
                    elif "primary" in msg:
                        raise IvaDuplicado("id", str(iva.id))
                    else:
                        raise IvaDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al crear iva")
        
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise IvaInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as ex:
            logger.info(f"Error repo en {ex}")
            raise ErrorDeRepositorio("Error inesperado al crear iva")

    async def update(self, iva_id: int, iva: Iva) -> Optional[Iva]:
        try:
            iva_sql = await self.db.get(IvaSQL, iva_id)
            if not iva_sql:
                return None

            cambios = False
            for field, value in vars(iva).items():
                if value is not None and hasattr(iva_sql, field):
                    setattr(iva_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(iva_sql)

            return self._to_domain(iva_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise IvaDuplicado("codigo", str(iva.codigo))
                    elif "primary" in msg:
                        raise IvaDuplicado("id", str(iva.id))
                    else:
                        raise IvaDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al actualizar iva")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar iva")


    async def delete(self, iva_id: int) -> None:
        try:
            iva_sql = await self.db.get(IvaSQL, iva_id)
            if not iva_sql:
                return

            await self.db.delete(iva_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("iva_id", str(iva_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar iva")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar iva")

    def _to_domain(self, iva_sql: IvaSQL) -> Iva:
        return Iva(
            id=iva_sql.id,
            codigo=iva_sql.codigo,
            descripcion=iva_sql.descripcion,
            porcentaje=iva_sql.porcentaje,
            discriminado=iva_sql.discriminado,
            porcentaje_sobre=iva_sql.porcentaje_sobre,
        )

    def _to_orm(self, iva: Iva) -> IvaSQL:
        return IvaSQL(
            id=iva.id,
            codigo=iva.codigo,
            descripcion=iva.descripcion,
            porcentaje=iva.porcentaje,
            discriminado=iva.discriminado,
            porcentaje_sobre=iva.porcentaje_sobre,
        )
