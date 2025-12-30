from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import CondicionTributaria as CondicionTributariaSQL
from app.domain.entities.condiciontributaria import CondicionTributaria
from app.domain.repository.condiciontributaria_repository_interfase import CondicionTributariaRepositoryInterface
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio

class CondicionTributariaRepositoryImpl(CondicionTributariaRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Optional[CondicionTributaria]:
        stmt = select(CondicionTributariaSQL).options(joinedload(CondicionTributariaSQL.tipo_impuesto)).where(CondicionTributariaSQL.id == id)
        result = await self.db.execute(stmt)
        sql_entity = result.scalar_one_or_none()
        return self._to_domain(sql_entity) if sql_entity else None

    async def get_all(self) -> List[CondicionTributaria]:
        stmt = select(CondicionTributariaSQL).options(joinedload(CondicionTributariaSQL.tipo_impuesto))
        result = await self.db.execute(stmt)
        sql_entities = result.scalars().all()
        return [self._to_domain(c) for c in sql_entities]

    async def create(self, condicion: CondicionTributaria) -> CondicionTributaria:
        try:
            sql_entity = self._to_orm(condicion)
            self.db.add(sql_entity)
            await self.db.commit()
            await self.db.refresh(sql_entity)
            return self._to_domain(sql_entity)
        except Exception:
            raise ErrorDeRepositorio("Error al crear condicion tributaria")

    async def update(self, id: int, condicion: CondicionTributaria) -> CondicionTributaria:
        try:
            sql_entity = await self.db.get(CondicionTributariaSQL, id)
            if not sql_entity:
                raise ErrorDeRepositorio("Condicion tributaria no encontrada")

            sql_entity.nombre = condicion.nombre
            sql_entity.descripcion = condicion.descripcion
            sql_entity.ambito = condicion.ambito
            sql_entity.tipo_impuesto_id = condicion.tipo_impuesto_id
            
            await self.db.commit()
            await self.db.refresh(sql_entity)
            return self._to_domain(sql_entity)
        except Exception:
            raise ErrorDeRepositorio("Error al actualizar condicion tributaria")

    async def delete(self, id: int) -> None:
        try:
            sql_entity = await self.db.get(CondicionTributariaSQL, id)
            if sql_entity:
                await self.db.delete(sql_entity)
                await self.db.commit()
        except Exception:
            raise ErrorDeRepositorio("Error al eliminar condicion tributaria")

    def _to_domain(self, sql_entity: CondicionTributariaSQL) -> CondicionTributaria:
        from app.domain.entities.tipoimpuesto import TipoImpuesto as TipoImpuestoDomain
        
        entity = CondicionTributaria(
            id=sql_entity.id,
            nombre=sql_entity.nombre,
            descripcion=sql_entity.descripcion,
            ambito=sql_entity.ambito,
            tipo_impuesto_id=sql_entity.tipo_impuesto_id
        )
        
        if hasattr(sql_entity, 'tipo_impuesto') and sql_entity.tipo_impuesto:
            entity.tipo_impuesto = TipoImpuestoDomain(
                id=sql_entity.tipo_impuesto.id,
                codigo_afip=sql_entity.tipo_impuesto.codigo_afip,
                nombre=sql_entity.tipo_impuesto.nombre,
                descripcion=sql_entity.tipo_impuesto.descripcion,
                tipo_aplicacion=sql_entity.tipo_impuesto.tipo_aplicacion,
                base_calculo=sql_entity.tipo_impuesto.base_calculo,
                ambito=sql_entity.tipo_impuesto.ambito,
                categoria=sql_entity.tipo_impuesto.categoria,
                porcentaje=sql_entity.tipo_impuesto.porcentaje,
                editable=sql_entity.tipo_impuesto.editable,
                obligatorio=sql_entity.tipo_impuesto.obligatorio,
                activo=sql_entity.tipo_impuesto.activo
            )
            
        return entity

    def _to_orm(self, domain_entity: CondicionTributaria) -> CondicionTributariaSQL:
        return CondicionTributariaSQL(
            id=domain_entity.id,
            nombre=domain_entity.nombre,
            descripcion=domain_entity.descripcion,
            ambito=domain_entity.ambito,
            tipo_impuesto_id=domain_entity.tipo_impuesto_id
        )
