# ✅ app/repositories/comprobanteimpuesto_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import ComprobanteImpuesto as ComprobanteImpuestoSQL
from app.domain.entities.comprobanteimpuesto import ComprobanteImpuesto
from app.domain.repository.comprobanteimpuesto_repository_interfase import ComprobanteImpuestoRepositoryInterface
from app.domain.exceptions.comprobanteimpuesto import ComprobanteImpuestoDuplicado, ComprobanteImpuestoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteImpuestoRepositoryImpl(ComprobanteImpuestoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comprobanteimpuesto_id: int) -> Optional[ComprobanteImpuesto]:
        stmt = select(ComprobanteImpuestoSQL).where(ComprobanteImpuestoSQL.id == comprobanteimpuesto_id)
        result = await self.db.execute(stmt)
        comprobanteimpuesto_sql = result.scalar_one_or_none()
        return self._to_domain(comprobanteimpuesto_sql) if comprobanteimpuesto_sql else None

    async def get_all(self) -> List[ComprobanteImpuesto]:
        stmt = select(ComprobanteImpuestoSQL)
        result = await self.db.execute(stmt)
        comprobanteimpuestos_sql = result.scalars().all()
        return [self._to_domain(c) for c in comprobanteimpuestos_sql]

    async def create(self, comprobanteimpuesto: ComprobanteImpuesto) -> ComprobanteImpuesto:
        try:
            obj_sql = self._to_orm(comprobanteimpuesto)
            self.db.add(obj_sql)
            await self.db.commit()
            await self.db.refresh(obj_sql)
            return self._to_domain(obj_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteImpuestoDuplicado("desconocido", "valor duplicado")
                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(comprobanteimpuesto.comprobante_id))
                    elif "tipo_impuesto_id" in msg:
                        raise ClaveForaneaInvalida("tipo_impuesto_id", str(comprobanteimpuesto.tipo_impuesto_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear comprobanteimpuesto")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteImpuestoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear comprobanteimpuesto")

    async def update(self, id: int, data: ComprobanteImpuesto) -> Optional[ComprobanteImpuesto]:
        try:
            obj_sql = await self.db.get(ComprobanteImpuestoSQL, id)
            if not obj_sql:
                return None

            cambios = False
            for field, value in vars(data).items():
                if value is not None and hasattr(obj_sql, field):
                    setattr(obj_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(obj_sql)

            return self._to_domain(obj_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteImpuestoDuplicado("desconocido", "valor duplicado")
                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(data.comprobante_id))
                    elif "tipo_impuesto_id" in msg:
                        raise ClaveForaneaInvalida("tipo_impuesto_id", str(data.tipo_impuesto_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar comprobanteimpuesto")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteImpuestoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobanteimpuesto")


    async def delete(self, id: int) -> None:
        try:
            obj_sql = await self.db.get(ComprobanteImpuestoSQL, id)
            if not obj_sql:
                return

            await self.db.delete(obj_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("comprobanteimpuesto_id", str(id))

            raise ErrorDeRepositorio("Error de integridad al eliminar comprobanteimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobanteimpuesto")


    def _to_domain(self, comprobanteimpuesto_sql: ComprobanteImpuestoSQL) -> ComprobanteImpuesto:
        return ComprobanteImpuesto(
            id=comprobanteimpuesto_sql.id,
            comprobante_id=comprobanteimpuesto_sql.comprobante_id,
            tipo_impuesto_id=comprobanteimpuesto_sql.tipo_impuesto_id,
            descripcion=comprobanteimpuesto_sql.descripcion,
            base_imponible=comprobanteimpuesto_sql.base_imponible,
            alicuota=comprobanteimpuesto_sql.alicuota,
            importe=comprobanteimpuesto_sql.importe
        )


    def _to_orm(self, comprobanteimpuesto: ComprobanteImpuesto) -> ComprobanteImpuestoSQL:
        return ComprobanteImpuestoSQL(
            id=comprobanteimpuesto.id,
            comprobante_id=comprobanteimpuesto.comprobante_id,
            tipo_impuesto_id=comprobanteimpuesto.tipo_impuesto_id,
            descripcion=comprobanteimpuesto.descripcion,
            base_imponible=comprobanteimpuesto.base_imponible,
            alicuota=comprobanteimpuesto.alicuota,
            importe=comprobanteimpuesto.importe
        )
