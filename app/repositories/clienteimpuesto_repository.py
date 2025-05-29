# ✅ app/repositories/clienteimpuesto_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import ClienteImpuesto as ClienteImpuestoSQL
from app.domain.entities.clienteimpuesto import ClienteImpuesto
from app.domain.repository.clienteimpuesto_repository_interfase import ClienteImpuestoRepositoryInterface
from app.domain.exceptions.clienteimpuesto import ClienteImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ClienteImpuestoRepositoryImpl(ClienteImpuestoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, clienteimpuesto_id: int) -> Optional[ClienteImpuesto]:
        stmt = select(ClienteImpuestoSQL).where(ClienteImpuestoSQL.id == clienteimpuesto_id)
        result = await self.db.execute(stmt)
        clienteimpuesto_sql = result.scalar_one_or_none()
        return self._to_domain(clienteimpuesto_sql) if clienteimpuesto_sql else None

    async def get_all(self) -> List[ClienteImpuesto]:
        stmt = select(ClienteImpuestoSQL)
        result = await self.db.execute(stmt)
        clienteimpuestos_sql = result.scalars().all()
        return [self._to_domain(c) for c in clienteimpuestos_sql]

    async def create(self, clienteimpuesto: ClienteImpuesto) -> ClienteImpuesto:
        try:
            clienteimpuesto_sql = self._to_orm(clienteimpuesto)
            self.db.add(clienteimpuesto_sql)
            await self.db.commit()
            await self.db.refresh(clienteimpuesto_sql)
            return self._to_domain(clienteimpuesto_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ClienteImpuestoDuplicado("duplicado", "combinación cliente_id + tipo_impuesto_id")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(clienteimpuesto.cliente_id))
                    elif "tipo_impuesto_id" in msg:
                        raise ClaveForaneaInvalida("tipo_impuesto_id", str(clienteimpuesto.tipo_impuesto_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear clienteimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear clienteimpuesto")

    async def update(self, clienteimpuesto_id: int, clienteimpuesto: ClienteImpuesto) -> Optional[ClienteImpuesto]:
        try:
            clienteimpuesto_sql = await self.db.get(ClienteImpuestoSQL, clienteimpuesto_id)
            if not clienteimpuesto_sql:
                return None

            cambios = False
            for field, value in vars(clienteimpuesto).items():
                if value is not None and hasattr(clienteimpuesto_sql, field):
                    setattr(clienteimpuesto_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(clienteimpuesto_sql)

            return self._to_domain(clienteimpuesto_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ClienteImpuestoDuplicado("duplicado", "combinación cliente_id + tipo_impuesto_id")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(clienteimpuesto.cliente_id))
                    elif "tipo_impuesto_id" in msg:
                        raise ClaveForaneaInvalida("tipo_impuesto_id", str(clienteimpuesto.tipo_impuesto_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar clienteimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar clienteimpuesto")


    async def delete(self, clienteimpuesto_id: int) -> None:
        try:
            clienteimpuesto_sql = await self.db.get(ClienteImpuestoSQL, clienteimpuesto_id)
            if not clienteimpuesto_sql:
                return

            await self.db.delete(clienteimpuesto_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("clienteimpuesto_id", str(clienteimpuesto_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar clienteimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar clienteimpuesto")


    def _to_domain(self, clienteimpuesto_sql: ClienteImpuestoSQL) -> ClienteImpuesto:
        return ClienteImpuesto(
            id=clienteimpuesto_sql.id,
            cliente_id=clienteimpuesto_sql.cliente_id,
            tipo_impuesto_id=clienteimpuesto_sql.tipo_impuesto_id,
            aplica=clienteimpuesto_sql.aplica,
            alicuota=clienteimpuesto_sql.alicuota,
            observaciones=clienteimpuesto_sql.observaciones
        )

    def _to_orm(self, clienteimpuesto: ClienteImpuesto) -> ClienteImpuestoSQL:
        return ClienteImpuestoSQL(
            id=clienteimpuesto.id,
            cliente_id=clienteimpuesto.cliente_id,
            tipo_impuesto_id=clienteimpuesto.tipo_impuesto_id,
            aplica=clienteimpuesto.aplica,
            alicuota=clienteimpuesto.alicuota,
            observaciones=clienteimpuesto.observaciones
        )
