# ✅ app/repositories/rolmenuitem_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import RolMenuItem as RolMenuItemSQL
from app.domain.entities.rolmenuitem import RolMenuItem
from app.domain.repository.rolmenuitem_repository_interfase import RolMenuItemRepositoryInterface
from app.domain.exceptions.rolmenuitem import RolMenuItemDuplicado, RolMenuItemInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class RolMenuItemRepositoryImpl(RolMenuItemRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, rolmenuitem_id: int) -> Optional[RolMenuItem]:
        stmt = select(RolMenuItemSQL).where(RolMenuItemSQL.id == rolmenuitem_id)
        result = await self.db.execute(stmt)
        rolmenuitem_sql = result.scalar_one_or_none()
        return self._to_domain(rolmenuitem_sql) if rolmenuitem_sql else None

    async def get_by_rol_id(self, value) -> Optional[RolMenuItem]:
        stmt = select(RolMenuItemSQL).where(RolMenuItemSQL.rol_id == value)
        result = await self.db.execute(stmt)
        rolmenuitem_sql = result.scalar_one_or_none()
        return self._to_domain(rolmenuitem_sql) if rolmenuitem_sql else None

    async def get_all(self) -> List[RolMenuItem]:
        stmt = select(RolMenuItemSQL)
        result = await self.db.execute(stmt)
        rolmenuitems_sql = result.scalars().all()
        return [self._to_domain(c) for c in rolmenuitems_sql]

    async def create(self, rolmenuitem: RolMenuItem) -> RolMenuItem:
        try:
            rolmenuitem_sql = self._to_orm(rolmenuitem)
            self.db.add(rolmenuitem_sql)
            await self.db.commit()
            await self.db.refresh(rolmenuitem_sql)
            return self._to_domain(rolmenuitem_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise RolMenuItemDuplicado("id", str(rolmenuitem.id))
                    else:
                        raise RolMenuItemDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "rol_id" in msg:
                        raise ClaveForaneaInvalida("rol_id", str(rolmenuitem.rol_id))
                    elif "menu_item_id" in msg:
                        raise ClaveForaneaInvalida("menu_item_id", str(rolmenuitem.menu_item_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear rolmenuitem")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise RolMenuItemInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear rolmenuitem")

    async def update(self, rolmenuitem_id: int, rolmenuitem: RolMenuItem) -> Optional[RolMenuItem]:
        try:
            rolmenuitem_sql = await self.db.get(RolMenuItemSQL, rolmenuitem_id)
            if not rolmenuitem_sql:
                return None

            cambios = False
            for field, value in vars(rolmenuitem).items():
                if value is not None and hasattr(rolmenuitem_sql, field):
                    setattr(rolmenuitem_sql, field, value)
                    cambios = True  # ✅ Marcar que hubo modificación

            if cambios:
                await self.db.commit()
                await self.db.refresh(rolmenuitem_sql)
                
            return self._to_domain(rolmenuitem_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    if "primary" in msg:
                        raise RolMenuItemDuplicado("id", str(rolmenuitem.id))
                    else:
                        raise RolMenuItemDuplicado("desconocido", "valor duplicado")

                elif error_code == 1452:
                    if "rol_id" in msg:
                        raise ClaveForaneaInvalida("rol_id", str(rolmenuitem.rol_id))
                    elif "menu_item_id" in msg:
                        raise ClaveForaneaInvalida("menu_item_id", str(rolmenuitem.menu_item_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar rolmenuitem")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise RolMenuItemInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as e:
            raise ErrorDeRepositorio("Error inesperado al actualizar rolmenuitem")


    async def delete(self, rolmenuitem_id: int) -> None:
        try:
            rolmenuitem_sql = await self.db.get(RolMenuItemSQL, rolmenuitem_id)
            if not rolmenuitem_sql:
                return

            await self.db.delete(rolmenuitem_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("rolmenuitem_id", str(rolmenuitem_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar rolmenuitem")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar rolmenuitem")

    def _to_domain(self, rolmenuitem_sql: RolMenuItemSQL) -> RolMenuItem:
        return RolMenuItem(
            rol_id=rolmenuitem_sql.rol_id,
            menu_item_id=rolmenuitem_sql.menu_item_id
        )

    def _to_orm(self, rolmenuitem: RolMenuItem) -> RolMenuItemSQL:
        return RolMenuItemSQL(
            rol_id=rolmenuitem.rol_id,
            menu_item_id=rolmenuitem.menu_item_id
        )



