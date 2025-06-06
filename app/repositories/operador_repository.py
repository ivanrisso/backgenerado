# ✅ app/repositories/operador_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Operador as OperadorSQL
from app.domain.entities.operador import Operador
from app.domain.repository.operador_repository_interfase import OperadorRepositoryInterface
from app.domain.exceptions.operador import OperadorDuplicado, OperadorInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class OperadorRepositoryImpl(OperadorRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, operador_id: int) -> Optional[Operador]:
        stmt = select(OperadorSQL).where(OperadorSQL.id == operador_id)
        result = await self.db.execute(stmt)
        operador_sql = result.scalar_one_or_none()
        return self._to_domain(operador_sql) if operador_sql else None

    async def get_all(self) -> List[Operador]:
        stmt = select(OperadorSQL)
        result = await self.db.execute(stmt)
        operadors_sql = result.scalars().all()
        return [self._to_domain(c) for c in operadors_sql]

    async def create(self, operador: Operador) -> Operador:
        try:
            operador_sql = self._to_orm(operador)
            self.db.add(operador_sql)
            await self.db.commit()
            await self.db.refresh(operador_sql)
            return self._to_domain(operador_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "cuit" in msg:
                        raise OperadorDuplicado("cuit", operador.cuit)
                    elif "primary" in msg:
                        raise OperadorDuplicado("id", str(operador.id))
                    else:
                        raise OperadorDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(operador.iva_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(operador.tipo_doc_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear operador")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise OperadorInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear operador")

    async def update(self, operador_id: int, operador: Operador) -> Optional[Operador]:
        try:
            operador_sql = await self.db.get(OperadorSQL, operador_id)
            if not operador_sql:
                return None

            cambios = False
            for field, value in vars(operador).items():
                if value is not None and hasattr(operador_sql, field):
                    setattr(operador_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(operador_sql)
                
            return self._to_domain(operador_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "cuit" in msg:
                        raise OperadorDuplicado("cuit", operador.cuit)
                    elif "primary" in msg:
                        raise OperadorDuplicado("id", str(operador.id))
                    else:
                        raise OperadorDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "iva_id" in msg:
                        raise ClaveForaneaInvalida("iva_id", str(operador.iva_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(operador.tipo_doc_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar operador")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise OperadorInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar operador")


    async def delete(self, operador_id: int) -> None:
        try:
            operador_sql = await self.db.get(OperadorSQL, operador_id)
            if not operador_sql:
                return

            await self.db.delete(operador_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("operador_id", str(operador_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar operador")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar operador")

    def _to_domain(self, operador_sql: OperadorSQL) -> Operador:
        return Operador(
            id=operador_sql.id,
            nombre=operador_sql.nombre,
            apellido=operador_sql.apellido,
            razon_social=operador_sql.razon_social,
            cuit=operador_sql.cuit,
            email=operador_sql.email,
            tipo_doc_id=operador_sql.tipo_doc_id,
            iva_id=operador_sql.iva_id,
        )

    def _to_orm(self, operador: Operador) -> OperadorSQL:
        return OperadorSQL(
            id=operador.id,
            nombre=operador.nombre,
            apellido=operador.apellido,
            razon_social=operador.razon_social,
            cuit=operador.cuit,
            email=operador.email,
            tipo_doc_id=operador.tipo_doc_id,
            iva_id=operador.iva_id,
        )
