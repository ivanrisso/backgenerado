# ✅ app/repositories/cliente_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Cliente as ClienteSQL
from app.domain.entities.cliente import Cliente
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface
from app.domain.exceptions.cliente import ClienteDuplicado, ClienteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ClienteRepositoryImpl(ClienteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        stmt = select(ClienteSQL).where(ClienteSQL.id == cliente_id)
        result = await self.db.execute(stmt)
        cliente_sql = result.scalar_one_or_none()
        return self._to_domain(cliente_sql) if cliente_sql else None

    async def get_all(self) -> List[Cliente]:
        stmt = select(ClienteSQL)
        result = await self.db.execute(stmt)
        clientes_sql = result.scalars().all()
        return [self._to_domain(c) for c in clientes_sql]

    async def create(self, cliente: Cliente) -> Cliente:
        try:
            cliente_sql = self._to_orm(cliente)
            self.db.add(cliente_sql)
            await self.db.commit()
            await self.db.refresh(cliente_sql)
            return self._to_domain(cliente_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "cuit" in msg:
                        raise ClienteDuplicado("cuit", cliente.cuit)
                    elif "primary" in msg:
                        raise ClienteDuplicado("id", str(cliente.id))
                    else:
                        raise ClienteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(cliente.iva_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(cliente.tipo_doc_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear cliente")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ClienteInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear cliente")

    async def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        try:
            cliente_sql = await self.db.get(ClienteSQL, cliente_id)
            if not cliente_sql:
                return None

            cambios = False
            for field, value in vars(cliente).items():
                if value is not None and hasattr(cliente_sql, field):
                    setattr(cliente_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(cliente_sql)
                
            return self._to_domain(cliente_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "cuit" in msg:
                        raise ClienteDuplicado("cuit", cliente.cuit)
                    elif "primary" in msg:
                        raise ClienteDuplicado("id", str(cliente.id))
                    else:
                        raise ClienteDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(cliente.iva_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(cliente.tipo_doc_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar cliente")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ClienteInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar cliente")


    async def delete(self, cliente_id: int) -> None:
        try:
            cliente_sql = await self.db.get(ClienteSQL, cliente_id)
            if not cliente_sql:
                return

            await self.db.delete(cliente_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("cliente_id", str(cliente_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar cliente")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar cliente")

    def _to_domain(self, cliente_sql: ClienteSQL) -> Cliente:
        return Cliente(
            id=cliente_sql.id,
            nombre=cliente_sql.nombre,
            apellido=cliente_sql.apellido,
            razon_social=cliente_sql.razon_social,
            cuit=cliente_sql.cuit,
            email=cliente_sql.email,
            tipo_doc_id=cliente_sql.tipo_doc_id,
            iva_id=cliente_sql.iva_id,
        )

    def _to_orm(self, cliente: Cliente) -> ClienteSQL:
        return ClienteSQL(
            id=cliente.id,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            razon_social=cliente.razon_social,
            cuit=cliente.cuit,
            email=cliente.email,
            tipo_doc_id=cliente.tipo_doc_id,
            iva_id=cliente.iva_id,
        )
