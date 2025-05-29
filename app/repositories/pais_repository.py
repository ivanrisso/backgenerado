# ✅ app/repositories/pais_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Optional, List

from app.infrastructure.db.orm_models import Pais as PaisSQL
from app.domain.entities.pais import Pais
from app.domain.repository.pais_repository_interfase import PaisRepositoryInterface
from app.domain.exceptions.pais import PaisDuplicado
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class PaisRepositoryImpl(PaisRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, pais_id: int) -> Optional[Pais]:
        stmt = select(PaisSQL).where(PaisSQL.id == pais_id)
        result = await self.db.execute(stmt)
        pais_sql = result.scalar_one_or_none()
        return self._to_domain(pais_sql) if pais_sql else None

    async def get_all(self) -> List[Pais]:
        stmt = select(PaisSQL)
        result = await self.db.execute(stmt)
        paiss_sql = result.scalars().all()
        return [self._to_domain(c) for c in paiss_sql]

    async def create(self, pais: Pais) -> Pais:
        try:
            pais_sql = self._to_orm(pais)
            self.db.add(pais_sql)
            await self.db.commit()
            await self.db.refresh(pais_sql)
            return self._to_domain(pais_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise PaisDuplicado("codigo", pais.codigo)
                    elif "primary" in msg:
                        raise PaisDuplicado("id", str(pais.id))
                    else:
                        raise PaisDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al crear país")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear país")


    async def update(self, pais_id: int, pais: Pais) -> Optional[Pais]:
        try:
            pais_sql = await self.db.get(PaisSQL, pais_id)
            if not pais_sql:
                return None

            cambios = False
            for field, value in vars(pais).items():
                if value is not None and hasattr(pais_sql, field):
                    setattr(pais_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(pais_sql)

            return self._to_domain(pais_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "codigo" in msg:
                        raise PaisDuplicado("codigo", pais.codigo)
                    elif "primary" in msg:
                        raise PaisDuplicado("id", str(pais.id))
                    else:
                        raise PaisDuplicado("desconocido", "valor duplicado")

            raise ErrorDeRepositorio("Error de integridad al actualizar país")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar país")


    async def delete(self, pais_id: int) -> None:
        try:
            pais_sql = await self.db.get(PaisSQL, pais_id)
            if not pais_sql:
                return

            await self.db.delete(pais_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("pais_id", str(pais_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar país")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar país")


    def _to_domain(self, pais_sql: PaisSQL) -> Pais:
        return Pais(
            id=pais_sql.id,
            codigo=pais_sql.codigo,
            nombre=pais_sql.nombre
        )

    def _to_orm(self, pais: Pais) -> PaisSQL:
        return PaisSQL(
            id=pais.id,
            codigo=pais.codigo,
            nombre=pais.nombre
        )
