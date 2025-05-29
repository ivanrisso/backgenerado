# ✅ app/repositories/tipoimpuesto_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import TipoImpuesto as TipoImpuestoSQL
from app.domain.entities.tipoimpuesto import TipoImpuesto
from app.domain.repository.tipoimpuesto_repository_interfase import TipoImpuestoRepositoryInterface
from app.domain.exceptions.tipoimpuesto import TipoImpuestoDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TipoImpuestoRepositoryImpl(TipoImpuestoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipoimpuesto_id: int) -> Optional[TipoImpuesto]:
        stmt = select(TipoImpuestoSQL).where(TipoImpuestoSQL.id == tipoimpuesto_id)
        result = await self.db.execute(stmt)
        tipoimpuesto_sql = result.scalar_one_or_none()
        return self._to_domain(tipoimpuesto_sql) if tipoimpuesto_sql else None

    async def get_all(self) -> List[TipoImpuesto]:
        stmt = select(TipoImpuestoSQL)
        result = await self.db.execute(stmt)
        tipoimpuestos_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipoimpuestos_sql]

    async def create(self, tipoimpuesto: TipoImpuesto) -> TipoImpuesto:
        try:
            tipoimpuesto_sql = self._to_orm(tipoimpuesto)
            self.db.add(tipoimpuesto_sql)
            await self.db.commit()
            await self.db.refresh(tipoimpuesto_sql)
            return self._to_domain(tipoimpuesto_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                logger.error(f"Integritt Error: {msg}")

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoImpuestoDuplicado("id", str(tipoimpuesto.id))
                    else:
                        raise TipoImpuestoDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear tipoimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear tipoimpuesto")

    async def update(self, tipoimpuesto_id: int, tipoimpuesto: TipoImpuesto) -> Optional[TipoImpuesto]:
        try:
            tipoimpuesto_sql = await self.db.get(TipoImpuestoSQL, tipoimpuesto_id)
            if not tipoimpuesto_sql:
                return None

            cambios = False
            for field, value in vars(tipoimpuesto).items():
                if value is not None and hasattr(tipoimpuesto_sql, field):
                    setattr(tipoimpuesto_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(tipoimpuesto_sql)
                
            return self._to_domain(tipoimpuesto_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise TipoImpuestoDuplicado("id", str(tipoimpuesto.id))
                    else:
                        raise TipoImpuestoDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar tipoimpuesto")

        except OperationalError:
            logger.info("acaaaaaa33333")
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            logger.info("acaaaaaa")
            raise ErrorDeRepositorio("Error inesperado al actualizar tipoimpuesto")


    async def delete(self, tipoimpuesto_id: int) -> None:
        try:
            tipoimpuesto_sql = await self.db.get(TipoImpuestoSQL, tipoimpuesto_id)
            if not tipoimpuesto_sql:
                return

            await self.db.delete(tipoimpuesto_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("tipoimpuesto_id", str(tipoimpuesto_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar tipoimpuesto")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar tipoimpuesto")

    def _to_domain(self, tipoimpuesto_sql: TipoImpuestoSQL) -> TipoImpuesto:
        return TipoImpuesto(
            id=tipoimpuesto_sql.id,
            codigo_afip=tipoimpuesto_sql.codigo_afip,
            nombre=tipoimpuesto_sql.nombre,
            descripcion=tipoimpuesto_sql.descripcion,
            tipo_aplicacion=tipoimpuesto_sql.tipo_aplicacion,
            base_calculo=tipoimpuesto_sql.base_calculo,
            porcentaje=tipoimpuesto_sql.porcentaje,
            editable=tipoimpuesto_sql.editable,
            obligatorio=tipoimpuesto_sql.obligatorio,
            activo=tipoimpuesto_sql.activo
        )

    def _to_orm(self, tipoimpuesto: TipoImpuesto) -> TipoImpuestoSQL:
        return TipoImpuestoSQL(
            id=tipoimpuesto.id,
            codigo_afip=tipoimpuesto.codigo_afip,
            nombre=tipoimpuesto.nombre,
            descripcion=tipoimpuesto.descripcion,
            tipo_aplicacion=tipoimpuesto.tipo_aplicacion,
            base_calculo=tipoimpuesto.base_calculo,
            porcentaje=tipoimpuesto.porcentaje,
            editable=tipoimpuesto.editable,
            obligatorio=tipoimpuesto.obligatorio,
            activo=tipoimpuesto.activo
        )
