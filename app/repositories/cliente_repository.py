# ✅ app/repositories/cliente_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
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
        stmt = (
            select(ClienteSQL)
            .options(
                joinedload(ClienteSQL.condicion_iva),
                joinedload(ClienteSQL.condicion_iibb)
            )
            .where(ClienteSQL.id == cliente_id)
        )
        result = await self.db.execute(stmt)
        cliente_sql = result.scalar_one_or_none()
        return self._to_domain(cliente_sql) if cliente_sql else None

    async def get_all(self) -> List[Cliente]:
        stmt = (
            select(ClienteSQL)
            .options(
                joinedload(ClienteSQL.condicion_iva),
                joinedload(ClienteSQL.condicion_iibb)
            )
        )
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
                    if "tipo_doc_id" in msg:
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
                    if "tipo_doc_id" in msg:
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
            
            # TODO: Handle cascading deletes or updates for impuestos if needed, 
            # though DB constraints usually handle blocking.
            
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

    async def get_deudores(self) -> List[tuple[Cliente, float]]:
        from sqlalchemy import func
        from app.infrastructure.db.orm_models import CuentaCorriente as CuentaCorrienteSQL
        
        stmt = (
            select(ClienteSQL, func.sum(CuentaCorrienteSQL.importe * CuentaCorrienteSQL.signo).label("saldo"))
            .join(CuentaCorrienteSQL, ClienteSQL.id == CuentaCorrienteSQL.cliente_id)
            .group_by(ClienteSQL.id)
            .having(func.sum(CuentaCorrienteSQL.importe * CuentaCorrienteSQL.signo) > 0)
            .options(
                joinedload(ClienteSQL.condicion_iva),
                joinedload(ClienteSQL.condicion_iibb)
            )
        )
        
        result = await self.db.execute(stmt)
        rows = result.all()
        
        return [(self._to_domain(cliente_sql), float(saldo)) for cliente_sql, saldo in rows]

    def _to_domain(self, cliente_sql: ClienteSQL) -> Cliente:
        from app.domain.entities.condiciontributaria import CondicionTributaria as CondicionTributariaDomain
        
        cliente = Cliente(
            id=cliente_sql.id,
            nombre=cliente_sql.nombre,
            apellido=cliente_sql.apellido,
            razon_social=cliente_sql.razon_social,
            cuit=cliente_sql.cuit,
            email=cliente_sql.email,
            tipo_doc_id=cliente_sql.tipo_doc_id,
            condicion_iva_id=cliente_sql.condicion_iva_id,
            condicion_iibb_id=cliente_sql.condicion_iibb_id,
            nro_iibb=cliente_sql.nro_iibb
        )

        if hasattr(cliente_sql, 'condicion_iva') and cliente_sql.condicion_iva:
            cliente.condicion_iva = CondicionTributariaDomain(
                id=cliente_sql.condicion_iva.id,
                nombre=cliente_sql.condicion_iva.nombre,
                descripcion=cliente_sql.condicion_iva.descripcion,
                ambito=cliente_sql.condicion_iva.ambito,
                tipo_impuesto_id=cliente_sql.condicion_iva.tipo_impuesto_id
            )
            
        if hasattr(cliente_sql, 'condicion_iibb') and cliente_sql.condicion_iibb:
            cliente.condicion_iibb = CondicionTributariaDomain(
                id=cliente_sql.condicion_iibb.id,
                nombre=cliente_sql.condicion_iibb.nombre,
                descripcion=cliente_sql.condicion_iibb.descripcion,
                ambito=cliente_sql.condicion_iibb.ambito,
                tipo_impuesto_id=cliente_sql.condicion_iibb.tipo_impuesto_id
            )

        return cliente

    def _to_orm(self, cliente: Cliente) -> ClienteSQL:
        return ClienteSQL(
            id=cliente.id,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            razon_social=cliente.razon_social,
            cuit=cliente.cuit,
            email=cliente.email,
            tipo_doc_id=cliente.tipo_doc_id,
            condicion_iva_id=cliente.condicion_iva_id,
            condicion_iibb_id=cliente.condicion_iibb_id,
            nro_iibb=cliente.nro_iibb
        )
