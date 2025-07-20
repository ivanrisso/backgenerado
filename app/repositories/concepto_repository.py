# ✅ app/repositories/concepto_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Concepto as ConceptoSQL
from app.domain.entities.concepto import Concepto
from app.domain.repository.concepto_repository_interfase import ConceptoRepositoryInterface
from app.domain.exceptions.concepto import ConceptoDuplicado, ConceptoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ConceptoRepositoryImpl(ConceptoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, concepto_id: int) -> Optional[Concepto]:
        stmt = select(ConceptoSQL).where(ConceptoSQL.id == concepto_id)
        result = await self.db.execute(stmt)
        concepto_sql = result.scalar_one_or_none()
        return self._to_domain(concepto_sql) if concepto_sql else None

    async def get_all(self) -> List[Concepto]:
        stmt = select(ConceptoSQL)
        result = await self.db.execute(stmt)
        conceptos_sql = result.scalars().all()
        return [self._to_domain(c) for c in conceptos_sql]

    async def create(self, concepto: Concepto) -> Concepto:
        try:
            concepto_sql = self._to_orm(concepto)
            self.db.add(concepto_sql)
            await self.db.commit()
            await self.db.refresh(concepto_sql)
            return self._to_domain(concepto_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise ConceptoDuplicado("codigo", concepto.codigo)
                    elif "primary" in msg:
                        raise ConceptoDuplicado("id", str(concepto.id))
                    else:
                        raise ConceptoDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al crear concepto")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ConceptoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear concepto")

    async def update(self, concepto_id: int, concepto: Concepto) -> Optional[Concepto]:
        try:
            concepto_sql = await self.db.get(ConceptoSQL, concepto_id)
            if not concepto_sql:
                return None

            cambios = False
            for field, value in vars(concepto).items():
                if value is not None and hasattr(concepto_sql, field):
                    setattr(concepto_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(concepto_sql)

            return self._to_domain(concepto_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise ConceptoDuplicado("codigo", concepto.codigo)
                    elif "primary" in msg:
                        raise ConceptoDuplicado("id", str(concepto.id))
                    else:
                        raise ConceptoDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al actualizar concepto")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ConceptoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar concepto")


    async def delete(self, concepto_id: int) -> None:
        try:
            concepto_sql = await self.db.get(ConceptoSQL, concepto_id)
            if not concepto_sql:
                return

            await self.db.delete(concepto_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("concepto_id", str(concepto_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar concepto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar concepto")


    def _to_domain(self, concepto_sql: ConceptoSQL) -> Concepto:
        return Concepto(
            id=concepto_sql.id,
            codigo=concepto_sql.codigo,
            descripcion=concepto_sql.descripcion,
            codigo_arca = concepto_sql.codigo_arca
        )


    def _to_orm(self, concepto: Concepto) -> ConceptoSQL:
        return ConceptoSQL(
            id=concepto.id,
            codigo=concepto.codigo,
            descripcion=concepto.descripcion,
            codigo_arca = concepto.codigo_arca
        )
