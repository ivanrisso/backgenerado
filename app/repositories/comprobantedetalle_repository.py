# ✅ app/repositories/comprobantedetalle_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import ComprobanteDetalle as ComprobanteDetalleSQL
from app.domain.entities.comprobantedetalle import ComprobanteDetalle
from app.domain.repository.comprobantedetalle_repository_interfase import ComprobanteDetalleRepositoryInterface
from app.domain.exceptions.comprobantedetalle import ComprobanteDetalleDuplicado, ComprobanteDetalleInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteDetalleRepositoryImpl(ComprobanteDetalleRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comprobantedetalle_id: int) -> Optional[ComprobanteDetalle]:
        stmt = select(ComprobanteDetalleSQL).where(ComprobanteDetalleSQL.id == comprobantedetalle_id)
        result = await self.db.execute(stmt)
        comprobantedetalle_sql = result.scalar_one_or_none()
        return self._to_domain(comprobantedetalle_sql) if comprobantedetalle_sql else None

    async def get_all(self) -> List[ComprobanteDetalle]:
        stmt = select(ComprobanteDetalleSQL)
        result = await self.db.execute(stmt)
        comprobantedetalles_sql = result.scalars().all()
        return [self._to_domain(c) for c in comprobantedetalles_sql]

    async def create(self, comprobantedetalle: ComprobanteDetalle, commit: bool = True) -> ComprobanteDetalle:
        try:
            obj_sql = self._to_orm(comprobantedetalle)
            self.db.add(obj_sql)
            
            if commit:
                await self.db.commit()
                await self.db.refresh(obj_sql)
            return self._to_domain(obj_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteDetalleDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(comprobantedetalle.comprobante_id))
                    elif "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(comprobantedetalle.iva_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear comprobantedetalle")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteDetalleInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear comprobantedetalle")

    async def update(self, id: int, data: ComprobanteDetalle, commit: bool = True) -> Optional[ComprobanteDetalle]:
        try:
            obj_sql = await self.db.get(ComprobanteDetalleSQL, id)
            if not obj_sql:
                return None

            cambios = False
            for field, value in vars(data).items():
                if value is not None and hasattr(obj_sql, field):
                    setattr(obj_sql, field, value)
                    cambios = True

            if cambios:
                if commit:
                    await self.db.commit()
                    await self.db.refresh(obj_sql)

            return self._to_domain(obj_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteDetalleDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(data.comprobante_id))
                    elif "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(data.iva_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar comprobantedetalle")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteDetalleInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobantedetalle")


    async def delete(self, id: int) -> None:
        try:
            obj_sql = await self.db.get(ComprobanteDetalleSQL, id)
            if not obj_sql:
                return

            await self.db.delete(obj_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("comprobantedetalle_id", str(id))

            raise ErrorDeRepositorio("Error de integridad al eliminar comprobantedetalle")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobantedetalle")

    # ✅ Obtener todos los detalles de un comprobante
    async def get_by_comprobante_id(self, comprobante_id: int) -> list[ComprobanteDetalle]:
        result = await self.session.execute(
            select(ComprobanteDetalleSQL).where(ComprobanteDetalleSQL.comprobante_id == comprobante_id)
        )
        return [self._to_domain(row) for row in result.scalars().all()]

    def _to_domain(self, comprobantedetalle_sql: ComprobanteDetalleSQL) -> ComprobanteDetalle:
        return ComprobanteDetalle(
            id=comprobantedetalle_sql.id,
            comprobante_id=comprobantedetalle_sql.comprobante_id,
            iva_id=comprobantedetalle_sql.iva_id,
            descripcion=comprobantedetalle_sql.descripcion,
            cantidad=comprobantedetalle_sql.cantidad,
            precio_unitario=comprobantedetalle_sql.precio_unitario,
            importe=comprobantedetalle_sql.importe,
            alicuota_iva=comprobantedetalle_sql.alicuota_iva,
            importe_iva=comprobantedetalle_sql.importe_iva            
        )


    def _to_orm(self, comprobantedetalle: ComprobanteDetalle) -> ComprobanteDetalleSQL:
        return ComprobanteDetalleSQL(
            id=comprobantedetalle.id,
            comprobante_id=comprobantedetalle.comprobante_id,
            iva_id=comprobantedetalle.iva_id,
            descripcion=comprobantedetalle.descripcion,
            cantidad=comprobantedetalle.cantidad,
            precio_unitario=comprobantedetalle.precio_unitario,
            importe=comprobantedetalle.importe,
            alicuota_iva=comprobantedetalle.alicuota_iva,
            importe_iva=comprobantedetalle.importe_iva
        )
