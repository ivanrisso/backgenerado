# ✅ app/repositories/domicilio_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Domicilio as DomicilioSQL
from app.domain.entities.domicilio import Domicilio
from app.domain.repository.domicilio_repository_interfase import DomicilioRepositoryInterface
from app.domain.exceptions.domicilio import DomicilioDuplicado, DomicilioInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class DomicilioRepositoryImpl(DomicilioRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, domicilio_id: int) -> Optional[Domicilio]:
        stmt = select(DomicilioSQL).where(DomicilioSQL.id == domicilio_id)
        result = await self.db.execute(stmt)
        domicilio_sql = result.scalar_one_or_none()
        return self._to_domain(domicilio_sql) if domicilio_sql else None

    async def get_all(self) -> List[Domicilio]:
        stmt = select(DomicilioSQL)
        result = await self.db.execute(stmt)
        domicilios_sql = result.scalars().all()
        return [self._to_domain(c) for c in domicilios_sql]

    async def create(self, domicilio: Domicilio) -> Domicilio:
        try:
            domicilio_sql = self._to_orm(domicilio)
            self.db.add(domicilio_sql)
            await self.db.commit()
            await self.db.refresh(domicilio_sql)
            return self._to_domain(domicilio_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise DomicilioDuplicado("id", str(domicilio.id))
                    else:
                        raise DomicilioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(domicilio.cliente_id))
                    elif "tipo_dom_id" in msg:
                        raise ClaveForaneaInvalida("tipo_dom_id", str(domicilio.tipo_dom_id))
                    elif "localidad_id" in msg:
                        raise ClaveForaneaInvalida("localidad_id", str(domicilio.localidad_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear domicilio")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise DomicilioInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear domicilio")

    async def update(self, domicilio_id: int, domicilio: Domicilio) -> Optional[Domicilio]:
        try:
            domicilio_sql = await self.db.get(DomicilioSQL, domicilio_id)
            if not domicilio_sql:
                return None

            cambios = False
            for field, value in vars(domicilio).items():
                if value is not None and hasattr(domicilio_sql, field):
                    setattr(domicilio_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(domicilio_sql)

            return self._to_domain(domicilio_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise DomicilioDuplicado("id", str(domicilio.id))
                    else:
                        raise DomicilioDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(domicilio.cliente_id))
                    elif "tipo_dom_id" in msg:
                        raise ClaveForaneaInvalida("tipo_dom_id", str(domicilio.tipo_dom_id))
                    elif "localidad_id" in msg:
                        raise ClaveForaneaInvalida("localidad_id", str(domicilio.localidad_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar domicilio")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise DomicilioInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar domicilio")


    async def delete(self, domicilio_id: int) -> None:
        try:
            domicilio_sql = await self.db.get(DomicilioSQL, domicilio_id)
            if not domicilio_sql:
                return

            await self.db.delete(domicilio_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("domicilio_id", str(domicilio_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar domicilio")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar domicilio")

    def _to_domain(self, domicilio_sql: DomicilioSQL) -> Domicilio:
        return Domicilio(
            id=domicilio_sql.id,
            calle=domicilio_sql.calle,
            numero=domicilio_sql.numero,
            cliente_id=domicilio_sql.cliente_id,
            tipo_dom_id=domicilio_sql.tipo_dom_id,
            localidad_id=domicilio_sql.localidad_id
        )

    def _to_orm(self, domicilio: Domicilio) -> DomicilioSQL:
        return DomicilioSQL(
            id=domicilio.id,
            calle=domicilio.calle,
            numero=domicilio.numero,
            cliente_id=domicilio.cliente_id,
            tipo_dom_id=domicilio.tipo_dom_id,
            localidad_id=domicilio.localidad_id
        )
