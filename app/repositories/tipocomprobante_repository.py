# ✅ app/repositories/tipocomprobante_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import TipoComprobante as TipoComprobanteSQL
from app.domain.entities.tipocomprobante import TipoComprobante
from app.domain.repository.tipocomprobante_repository_interfase import TipoComprobanteRepositoryInterface
from app.domain.exceptions.tipocomprobante import TipoComprobanteDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoComprobanteRepositoryImpl(TipoComprobanteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipocomprobante_id: int) -> Optional[TipoComprobante]:
        stmt = select(TipoComprobanteSQL).where(TipoComprobanteSQL.id == tipocomprobante_id)
        result = await self.db.execute(stmt)
        tipocomprobante_sql = result.scalar_one_or_none()
        return self._to_domain(tipocomprobante_sql) if tipocomprobante_sql else None

    async def get_all(self) -> List[TipoComprobante]:
        stmt = select(TipoComprobanteSQL)
        result = await self.db.execute(stmt)
        tipocomprobantes_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipocomprobantes_sql]

    async def create(self, tipocomprobante: TipoComprobante) -> TipoComprobante:
        try:
            tipocomprobante_sql = self._to_orm(tipocomprobante)
            self.db.add(tipocomprobante_sql)
            await self.db.commit()
            await self.db.refresh(tipocomprobante_sql)
            return self._to_domain(tipocomprobante_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoComprobanteDuplicado("id", str(tipocomprobante.id))
                    else:
                        raise TipoComprobanteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear tipocomprobante")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipocomprobante")

    async def update(self, tipocomprobante_id: int, tipocomprobante: TipoComprobante) -> Optional[TipoComprobante]:
        try:
            tipocomprobante_sql = await self.db.get(TipoComprobanteSQL, tipocomprobante_id)
            if not tipocomprobante_sql:
                return None

            cambios = False
            for field, value in vars(tipocomprobante).items():
                if value is not None and hasattr(tipocomprobante_sql, field):
                    setattr(tipocomprobante_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(tipocomprobante_sql)
                
            return self._to_domain(tipocomprobante_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoComprobanteDuplicado("id", str(tipocomprobante.id))
                    else:
                        raise TipoComprobanteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar tipocomprobante")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar tipocomprobante")


    async def delete(self, tipocomprobante_id: int) -> None:
        try:
            tipocomprobante_sql = await self.db.get(TipoComprobanteSQL, tipocomprobante_id)
            if not tipocomprobante_sql:
                return

            await self.db.delete(tipocomprobante_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("tipocomprobante_id", str(tipocomprobante_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar tipocomprobante")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipocomprobante")

    def _to_domain(self, tipocomprobante_sql: TipoComprobanteSQL) -> TipoComprobante:
        return TipoComprobante(
            id=tipocomprobante_sql.id,
            codigo=tipocomprobante_sql.codigo,
            descripcion=tipocomprobante_sql.descripcion,
            es_fiscal=tipocomprobante_sql.es_fiscal
        )
        

    def _to_orm(self, tipocomprobante: TipoComprobante) -> TipoComprobanteSQL:
        return TipoComprobanteSQL(
            id=tipocomprobante.id,
            codigo=tipocomprobante.codigo,
            descripcion=tipocomprobante.descripcion,
            es_fiscal=tipocomprobante.es_fiscal
        )
