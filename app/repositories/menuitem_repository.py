# ✅ app/repositories/menuitem_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import MenuItem as MenuItemSQL
from app.domain.entities.menuitem import MenuItem
from app.domain.repository.menuitem_repository_interfase import MenuItemRepositoryInterface
from app.domain.exceptions.menuitem import MenuItemDuplicado, MenuItemInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class MenuItemRepositoryImpl(MenuItemRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, menuitem_id: int) -> Optional[MenuItem]:
        stmt = select(MenuItemSQL).where(MenuItemSQL.id == menuitem_id)
        result = await self.db.execute(stmt)
        menuitem_sql = result.scalar_one_or_none()
        return self._to_domain(menuitem_sql) if menuitem_sql else None

    async def get_all(self) -> List[MenuItem]:
        stmt = select(MenuItemSQL)
        result = await self.db.execute(stmt)
        menuitems_sql = result.scalars().all()
        return [self._to_domain(c) for c in menuitems_sql]

    async def create(self, menuitem: MenuItem) -> MenuItem:
        try:
            menuitem_sql = self._to_orm(menuitem)
            self.db.add(menuitem_sql)
            await self.db.commit()
            await self.db.refresh(menuitem_sql)
            return self._to_domain(menuitem_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise MenuItemDuplicado("nombre", menuitem.nombre)

                elif error_code == 1452:
                    if "parent_id" in msg:
                        raise ClaveForaneaInvalida("parent_id", str(menuitem.parent_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al crear menuitem")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise MenuItemInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al crear menuitem")

    async def update(self, menuitem_id: int, menuitem: MenuItem) -> Optional[MenuItem]:
        try:
            menuitem_sql = await self.db.get(MenuItemSQL, menuitem_id)
            if not menuitem_sql:
                return None

            cambios = False
            for field, value in vars(menuitem).items():
                if value is not None and hasattr(menuitem_sql, field):
                    setattr(menuitem_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(menuitem_sql)

            return self._to_domain(menuitem_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise MenuItemDuplicado("nombre", menuitem.nombre)

                elif error_code == 1452:
                    if "parent_id" in msg:
                        raise ClaveForaneaInvalida("parent_id", str(menuitem.parent_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar menuitem")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise MenuItemInvalido(msg)        
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar menuitem")

    async def delete(self, menuitem_id: int) -> None:
        try:
            menuitem_sql = await self.db.get(MenuItemSQL, menuitem_id)
            if not menuitem_sql:
                return

            await self.db.delete(menuitem_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("menuitem_id", str(menuitem_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar menuitem")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar menuitem")

    def _to_domain(self, menuitem_sql: MenuItemSQL) -> MenuItem:
        return MenuItem(
            id=menuitem_sql.id,
            nombre=menuitem_sql.nombre,
            path=menuitem_sql.path,
            parent_id=menuitem_sql.parent_id
        )

    def _to_orm(self, menuitem: MenuItem) -> MenuItemSQL:
        return MenuItemSQL(
            id=menuitem.id,
            nombre=menuitem.nombre,
            path=menuitem.path,
            parent_id=menuitem.parent_id
        )
