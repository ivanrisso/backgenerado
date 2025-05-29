# ✅ app/repositories/cuentacorriente_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import CuentaCorriente as CuentaCorrienteSQL
from app.domain.entities.cuentacorriente import CuentaCorriente
from app.domain.repository.cuentacorriente_repository_interfase import CuentaCorrienteRepositoryInterface
from app.domain.exceptions.cuentacorriente import CuentaCorrienteDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class CuentaCorrienteRepositoryImpl(CuentaCorrienteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, cuentacorriente_id: int) -> Optional[CuentaCorriente]:
        stmt = select(CuentaCorrienteSQL).where(CuentaCorrienteSQL.id == cuentacorriente_id)
        result = await self.db.execute(stmt)
        cuentacorriente_sql = result.scalar_one_or_none()
        return self._to_domain(cuentacorriente_sql) if cuentacorriente_sql else None
    
    async def get_by_cuentacorriente_id(self, value) -> Optional[CuentaCorriente]:
        stmt = select(CuentaCorrienteSQL).where(CuentaCorrienteSQL.cuentacorriente_id == value)
        result = await self.db.execute(stmt)
        cuentacorriente_sql = result.scalar_one_or_none()
        return self._to_domain(cuentacorriente_sql) if cuentacorriente_sql else None

    async def get_all(self) -> List[CuentaCorriente]:
        stmt = select(CuentaCorrienteSQL)
        result = await self.db.execute(stmt)
        cuentacorrientes_sql = result.scalars().all()
        return [self._to_domain(c) for c in cuentacorrientes_sql]

    async def create(self, cuentacorriente: CuentaCorriente) -> CuentaCorriente:
        try:
            cuentacorriente_sql = self._to_orm(cuentacorriente)
            self.db.add(cuentacorriente_sql)
            await self.db.commit()
            await self.db.refresh(cuentacorriente_sql)
            return self._to_domain(cuentacorriente_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise CuentaCorrienteDuplicado("id", str(cuentacorriente.id))
                    else:
                        raise CuentaCorrienteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(cuentacorriente.cliente_id))
                    elif "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(cuentacorriente.comprobante_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear cuentacorriente")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear cuentacorriente")

    async def update(self, cuentacorriente_id: int, cuentacorriente: CuentaCorriente) -> Optional[CuentaCorriente]:
        try:
            cuentacorriente_sql = await self.db.get(CuentaCorrienteSQL, cuentacorriente_id)
            if not cuentacorriente_sql:
                return None

            cambios = False
            for field, value in vars(cuentacorriente).items():
                if value is not None and hasattr(cuentacorriente_sql, field):
                    setattr(cuentacorriente_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(cuentacorriente_sql)

            return self._to_domain(cuentacorriente_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise CuentaCorrienteDuplicado("id", str(cuentacorriente.id))
                    else:
                        raise CuentaCorrienteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(cuentacorriente.cliente_id))
                    elif "comprobante_id" in msg:
                        raise ClaveForaneaInvalida("comprobante_id", str(cuentacorriente.comprobante_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar cuentacorriente")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar cuentacorriente")


    async def delete(self, cuentacorriente_id: int) -> None:
        try:
            cuentacorriente_sql = await self.db.get(CuentaCorrienteSQL, cuentacorriente_id)
            if not cuentacorriente_sql:
                return

            await self.db.delete(cuentacorriente_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    # No se puede eliminar por dependencia en clave foránea (ej. comprobante_id en otra tabla)
                    raise ClaveForaneaInvalida("cuentacorriente_id", str(cuentacorriente_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar cuentacorriente")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar cuentacorriente")


    def _to_domain(self, cuentacorriente_sql: CuentaCorrienteSQL) -> CuentaCorriente:
        return CuentaCorriente(
            id=cuentacorriente_sql.id,
            cliente_id=cuentacorriente_sql.cliente_id,
            comprobante_id=cuentacorriente_sql.comprobante_id,
            fecha=cuentacorriente_sql.fecha,
            tipo=cuentacorriente_sql.tipo,
            descripcion=cuentacorriente_sql.descripcion,
            importe=cuentacorriente_sql.importe,
            signo=cuentacorriente_sql.signo,
            saldo=cuentacorriente_sql.saldo
        )


    def _to_orm(self, cuentacorriente: CuentaCorriente) -> CuentaCorrienteSQL:
        return CuentaCorrienteSQL(
            id=cuentacorriente.id,
            cliente_id=cuentacorriente.cliente_id,
            comprobante_id=cuentacorriente.comprobante_id,
            fecha=cuentacorriente.fecha,
            tipo=cuentacorriente.tipo,
            descripcion=cuentacorriente.descripcion,
            importe=cuentacorriente.importe,
            signo=cuentacorriente.signo,
            saldo=cuentacorriente.saldo
        )



