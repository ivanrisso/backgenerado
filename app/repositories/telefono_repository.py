# ✅ app/repositories/telefono_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Telefono as TelefonoSQL
from app.domain.entities.telefono import Telefono
from app.domain.repository.telefono_repository_interfase import TelefonoRepositoryInterface
from app.domain.exceptions.telefono import TelefonoDuplicado, TelefonoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class TelefonoRepositoryImpl(TelefonoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, telefono_id: int) -> Optional[Telefono]:
        stmt = select(TelefonoSQL).where(TelefonoSQL.id == telefono_id)
        result = await self.db.execute(stmt)
        telefono_sql = result.scalar_one_or_none()
        return self._to_domain(telefono_sql) if telefono_sql else None

    async def get_all(self) -> List[Telefono]:
        stmt = select(TelefonoSQL)
        result = await self.db.execute(stmt)
        telefonos_sql = result.scalars().all()
        return [self._to_domain(c) for c in telefonos_sql]

    async def get_by_domicilio(self, domicilio_id: int) -> List[Telefono]:
        stmt = select(TelefonoSQL).where(TelefonoSQL.domicilio_id == domicilio_id)
        result = await self.db.execute(stmt)
        telefonos_sql = result.scalars().all()
        return [self._to_domain(c) for c in telefonos_sql]

    async def create(self, telefono: Telefono) -> Telefono:
        try:
            telefono_sql = self._to_orm(telefono)
            self.db.add(telefono_sql)
            await self.db.commit()
            await self.db.refresh(telefono_sql)
            return self._to_domain(telefono_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "domicilio_id" in msg:
                        raise TelefonoDuplicado("domicilio_id", telefono.domicilio_id)
                    elif "tipo_tel_id" in msg:
                        raise TelefonoDuplicado("tipo_tel_id", str(telefono.tipo_tel_id))                    
                    elif "primary" in msg:
                        raise TelefonoDuplicado("id", str(telefono.id))
                    else:
                        raise TelefonoDuplicado("desconocido", "valor duplicado")
                    
                elif error_code == 1452:
                    if "domicilio_id" in msg:
                        raise ClaveForaneaInvalida("domicilio_id", str(telefono.domicilio_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(telefono.tipo_doc_id))                    
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear telefono")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TelefonoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear telefono")

    async def update(self, telefono_id: int, telefono: Telefono) -> Optional[Telefono]:
        try:
            telefono_sql = await self.db.get(TelefonoSQL, telefono_id)
            if not telefono_sql:
                return None

            cambios = False
            for field, value in vars(telefono).items():
                if value is not None and hasattr(telefono_sql, field):
                    setattr(telefono_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(telefono_sql)
                
            return self._to_domain(telefono_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "domicilio_id" in msg:
                        raise TelefonoDuplicado("domicilio_id", telefono.domicilio_id)
                    elif "tipo_tel_id" in msg:
                        raise TelefonoDuplicado("tipo_tel_id", str(telefono.tipo_tel_id))                    
                    elif "primary" in msg:
                        raise TelefonoDuplicado("id", str(telefono.id))
                    else:
                        raise TelefonoDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "domicilio_id" in msg:
                        raise ClaveForaneaInvalida("domicilio_id", str(telefono.domicilio_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(telefono.tipo_doc_id))                    
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar telefono")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise TelefonoInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar telefono")


    async def delete(self, telefono_id: int) -> None:
        try:
            telefono_sql = await self.db.get(TelefonoSQL, telefono_id)
            if not telefono_sql:
                return

            await self.db.delete(telefono_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    if "domicilio_id" in msg:
                        raise ClaveForaneaInvalida("domicilio_id", "domicilio_id")
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id","tipo_doc_id")                    
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")
                
            raise ErrorDeRepositorio("Error de integridad al eliminar telefono")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar telefono")

    def _to_domain(self, telefono_sql: TelefonoSQL) -> Telefono:
        return Telefono(
            id=telefono_sql.id,
            tipo_tel_id=telefono_sql.tipo_tel_id,
            prefijo=telefono_sql.prefijo,
            numero=telefono_sql.numero,
            domicilio_id=telefono_sql.domicilio_id
        )
        
    def _to_orm(self, telefono: Telefono) -> TelefonoSQL:
        return TelefonoSQL(
            id=telefono.id,
            tipo_tel_id=telefono.tipo_tel_id,
            prefijo=telefono.prefijo,
            numero=telefono.numero,
            domicilio_id=telefono.domicilio_id
        )
