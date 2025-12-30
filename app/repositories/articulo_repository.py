from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from app.infrastructure.db.orm_models import Articulo as ArticuloSQL
from app.domain.entities.articulo import Articulo
from app.domain.repository.articulo_repository_interfase import ArticuloRepositoryInterface
from app.domain.exceptions.articulo import ArticuloDuplicado, ArticuloInvalido
from app.domain.exceptions.base import ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

class ArticuloRepositoryImpl(ArticuloRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, articulo_id: int) -> Optional[Articulo]:
        stmt = select(ArticuloSQL).options(
            joinedload(ArticuloSQL.impuesto_venta),
            joinedload(ArticuloSQL.impuesto_compra)
        ).where(ArticuloSQL.id == articulo_id)
        result = await self.db.execute(stmt)
        sql_obj = result.scalar_one_or_none()
        return self._to_domain(sql_obj) if sql_obj else None

    async def get_all(self) -> List[Articulo]:
        stmt = select(ArticuloSQL).options(
            joinedload(ArticuloSQL.impuesto_venta),
            joinedload(ArticuloSQL.impuesto_compra)
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(obj) for obj in result.scalars().all()]

    async def get_by_codigo(self, codigo: str) -> Optional[Articulo]:
        stmt = select(ArticuloSQL).where(ArticuloSQL.codigo == codigo)
        result = await self.db.execute(stmt)
        sql_obj = result.scalar_one_or_none()
        return self._to_domain(sql_obj) if sql_obj else None

    async def create(self, articulo: Articulo) -> Articulo:
        try:
            sql_obj = self._to_orm(articulo)
            self.db.add(sql_obj)
            await self.db.commit()
            await self.db.refresh(sql_obj)
            return await self.get_by_id(sql_obj.id)
        except IntegrityError as e:
            await self.db.rollback()
            if "UNIQUE" in str(e.orig).upper() or "1062" in str(e.orig):
                raise ArticuloDuplicado("codigo", articulo.codigo)
            if "FOREIGN KEY" in str(e.orig).upper() or "1452" in str(e.orig):
                raise ClaveForaneaInvalida("impuesto_venta_id / impuesto_compra_id")
            raise ErrorDeRepositorio(str(e))

    async def update(self, articulo_id: int, articulo: Articulo) -> Optional[Articulo]:
        sql_obj = await self.db.get(ArticuloSQL, articulo_id)
        if not sql_obj:
            return None
        
        for key, value in vars(articulo).items():
            if value is not None and hasattr(sql_obj, key) and not key.startswith("_"):
                setattr(sql_obj, key, value)
        
        try:
            await self.db.commit()
            return await self.get_by_id(articulo_id)
        except IntegrityError as e:
            await self.db.rollback()
            if "UNIQUE" in str(e.orig).upper():
                raise ArticuloDuplicado("codigo", articulo.codigo)
            raise ErrorDeRepositorio(str(e))

    async def delete(self, articulo_id: int) -> bool:
        sql_obj = await self.db.get(ArticuloSQL, articulo_id)
        if not sql_obj:
            return False
        await self.db.delete(sql_obj)
        await self.db.commit()
        return True

    def _to_domain(self, sql_obj: ArticuloSQL) -> Articulo:
        # Import inside to avoid circular deps if needed, 
        # but TipoImpuesto is already imported in articulo_domain.
        from app.domain.entities.tipoimpuesto import TipoImpuesto as TipoImpuestoDomain

        return Articulo(
            id=sql_obj.id,
            codigo=sql_obj.codigo,
            nombre=sql_obj.nombre,
            descripcion=sql_obj.descripcion,
            precio_venta=sql_obj.precio_venta,
            precio_costo=sql_obj.precio_costo,
            tipo=sql_obj.tipo,
            activo=sql_obj.activo,
            impuesto_venta_id=sql_obj.impuesto_venta_id,
            impuesto_compra_id=sql_obj.impuesto_compra_id,
            # Map relations if loaded
            impuesto_venta=self._map_tax(sql_obj.impuesto_venta),
            impuesto_compra=self._map_tax(sql_obj.impuesto_compra)
        )

    def _map_tax(self, sql_tax):
        if not sql_tax: return None
        from app.domain.entities.tipoimpuesto import TipoImpuesto
        return TipoImpuesto(
            id=sql_tax.id,
            codigo_afip=sql_tax.codigo_afip,
            nombre=sql_tax.nombre,
            descripcion=sql_tax.descripcion,
            tipo_uso=sql_tax.tipo_uso,
            # ... and so on. Better if we add a helper in the other repo or just map essentials.
            # For simplicity, returning essentials.
        )

    def _to_orm(self, articulo: Articulo) -> ArticuloSQL:
        return ArticuloSQL(
            codigo=articulo.codigo,
            nombre=articulo.nombre,
            descripcion=articulo.descripcion,
            precio_venta=articulo.precio_venta,
            precio_costo=articulo.precio_costo,
            tipo=articulo.tipo,
            activo=articulo.activo,
            impuesto_venta_id=articulo.impuesto_venta_id,
            impuesto_compra_id=articulo.impuesto_compra_id
        )
