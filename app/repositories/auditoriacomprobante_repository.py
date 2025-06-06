# ✅ app/repositories/auditoriacomprobante_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import AuditoriaComprobante as AuditoriaComprobanteSQL
from app.domain.entities.auditoriacomprobante import AuditoriaComprobante
from app.domain.repository.auditoriacomprobante_repository_interfase import AuditoriaComprobanteRepositoryInterface
from app.domain.exceptions.auditoriacomprobante import AuditoriaComprobanteDuplicado, AuditoriaComprobanteInvalido 
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class AuditoriaComprobanteRepositoryImpl(AuditoriaComprobanteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, auditoriacomprobante_id: int) -> Optional[AuditoriaComprobante]:
        stmt = select(AuditoriaComprobanteSQL).where(AuditoriaComprobanteSQL.id == auditoriacomprobante_id)
        result = await self.db.execute(stmt)
        auditoriacomprobante_sql = result.scalar_one_or_none()
        return self._to_domain(auditoriacomprobante_sql) if auditoriacomprobante_sql else None

    async def get_all(self) -> List[AuditoriaComprobante]:
        stmt = select(AuditoriaComprobanteSQL)
        result = await self.db.execute(stmt)
        auditoriacomprobantes_sql = result.scalars().all()
        return [self._to_domain(c) for c in auditoriacomprobantes_sql]

    async def create(self, auditoriacomprobante: AuditoriaComprobante) -> AuditoriaComprobante:
        try:
            auditoriacomprobante_sql = self._to_orm(auditoriacomprobante)
            self.db.add(auditoriacomprobante_sql)
            await self.db.commit()
            await self.db.refresh(auditoriacomprobante_sql)
            return self._to_domain(auditoriacomprobante_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise AuditoriaComprobanteDuplicado("duplicado", "id o combinación existente")

                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(auditoriacomprobante.comprobante_id))
                    elif "usuario_id" in msg:
                        raise ClaveForaneaInvalida("usuario_id", str(auditoriacomprobante.usuario_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear auditoriacomprobante")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise AuditoriaComprobanteInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear auditoriacomprobante")


    async def update(self, auditoriacomprobante_id: int, auditoriacomprobante: AuditoriaComprobante) -> Optional[AuditoriaComprobante]:
        try:
            auditoriacomprobante_sql = await self.db.get(AuditoriaComprobanteSQL, auditoriacomprobante_id)
            if not auditoriacomprobante_sql:
                return None

            cambios = False
            for field, value in vars(auditoriacomprobante).items():
                if value is not None and hasattr(auditoriacomprobante_sql, field):
                    setattr(auditoriacomprobante_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(auditoriacomprobante_sql)

            return self._to_domain(auditoriacomprobante_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise AuditoriaComprobanteDuplicado("duplicado", "id o combinación existente")

                elif error_code == 1452:
                    if "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(auditoriacomprobante.comprobante_id))
                    elif "usuario_id" in msg:
                        raise ClaveForaneaInvalida("usuario_id", str(auditoriacomprobante.usuario_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar auditoriacomprobante")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise AuditoriaComprobanteInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar auditoriacomprobante")


    async def delete(self, auditoriacomprobante_id: int) -> None:
        try:
            auditoriacomprobante_sql = await self.db.get(AuditoriaComprobanteSQL, auditoriacomprobante_id)
            if not auditoriacomprobante_sql:
                return

            await self.db.delete(auditoriacomprobante_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("auditoriacomprobante_id", str(auditoriacomprobante_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar auditoriacomprobante")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar auditoriacomprobante")


    def _to_domain(self, auditoriacomprobante_sql: AuditoriaComprobanteSQL) -> AuditoriaComprobante:
        return AuditoriaComprobante(
            id=auditoriacomprobante_sql.id,
            comprobante_id=auditoriacomprobante_sql.comprobante_id,
            usuario_id=auditoriacomprobante_sql.usuario_id,
            accion=auditoriacomprobante_sql.accion,
            detalle=auditoriacomprobante_sql.detalle,
            ip_origen=auditoriacomprobante_sql.ip_origen,
            fecha=auditoriacomprobante_sql.fecha
        )


    def _to_orm(self, auditoriacomprobante: AuditoriaComprobante) -> AuditoriaComprobanteSQL:
        return AuditoriaComprobanteSQL(
            id=auditoriacomprobante.id,
            comprobante_id=auditoriacomprobante.comprobante_id,
            usuario_id=auditoriacomprobante.usuario_id,
            accion=auditoriacomprobante.accion,
            detalle=auditoriacomprobante.detalle,
            ip_origen=auditoriacomprobante.ip_origen,
            fecha=auditoriacomprobante.fecha
        )
