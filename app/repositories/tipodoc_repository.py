# ✅ app/repositories/tipodoc_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import TipoDoc as TipoDocSQL
from app.domain.entities.tipodoc import TipoDoc
from app.domain.repository.tipodoc_repository_interfase import TipoDocRepositoryInterface
from app.domain.exceptions.tipodoc import TipoDocDuplicado, TipoDocInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

class TipoDocRepositoryImpl(TipoDocRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipodoc_id: int) -> Optional[TipoDoc]:
        stmt = select(TipoDocSQL).where(TipoDocSQL.id == tipodoc_id)
        result = await self.db.execute(stmt)
        tipodoc_sql = result.scalar_one_or_none()
        return self._to_domain(tipodoc_sql) if tipodoc_sql else None

    async def get_all(self) -> List[TipoDoc]:
        stmt = select(TipoDocSQL)
        result = await self.db.execute(stmt)
        tipodocs_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipodocs_sql]

    async def create(self, tipodoc: TipoDoc) -> TipoDoc:
        try:
            tipodoc_sql = self._to_orm(tipodoc)
            self.db.add(tipodoc_sql)
            await self.db.commit()
            await self.db.refresh(tipodoc_sql)
            return self._to_domain(tipodoc_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                logger.error(f"Integritt Error: {msg}")

                if error_code == 1062:
                    if "cuit" in msg:
                        raise TipoDocDuplicado("cuit", tipodoc.cuit)
                    elif "primary" in msg:
                        raise TipoDocDuplicado("id", str(tipodoc.id))
                    else:
                        raise TipoDocDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear tipodoc")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TipoDocInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipodoc")

    async def update(self, tipodoc_id: int, tipodoc: TipoDoc) -> Optional[TipoDoc]:
        try:
            tipodoc_sql = await self.db.get(TipoDocSQL, tipodoc_id)

            if not tipodoc_sql:
                return None

            cambios = False
            for field, value in vars(tipodoc).items():
                if value is not None and hasattr(tipodoc_sql, field):
                    setattr(tipodoc_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(tipodoc_sql)
                
            return self._to_domain(tipodoc_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "cuit" in msg:
                        raise TipoDocDuplicado("cuit", tipodoc.cuit)
                    elif "primary" in msg:
                        raise TipoDocDuplicado("id", str(tipodoc.id))
                    else:
                        raise TipoDocDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar tipodoc")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TipoDocInvalido(msg)        
        except OperationalError:
            logger.info("acaaaaaa33333")
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            logger.info("acaaaaaa")
            raise ErrorDeRepositorio("Error inesperado al actualizar tipodoc")


    async def delete(self, tipodoc_id: int) -> None:
        try:
            tipodoc_sql = await self.db.get(TipoDocSQL, tipodoc_id)
            if not tipodoc_sql:
                return

            await self.db.delete(tipodoc_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("tipodoc_id", str(tipodoc_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar tipodoc")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipodoc")

    def _to_domain(self, tipodoc_sql: TipoDocSQL) -> TipoDoc:
        return TipoDoc(
            id=tipodoc_sql.id,
            tipo_doc_nombre=tipodoc_sql.tipo_doc_nombre,
            habilitado=tipodoc_sql.habilitado,
            codigo_arca = tipodoc_sql.codigo_arca
        )

    def _to_orm(self, tipodoc: TipoDoc) -> TipoDocSQL:
        return TipoDocSQL(
            id=tipodoc.id,
            tipo_doc_nombre=tipodoc.tipo_doc_nombre,
            habilitado=tipodoc.habilitado,
            codigo_arca = tipodoc.codigo_arca
        )
