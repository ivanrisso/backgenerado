# ✅ app/repositories/tipoimpuesto_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import (
    TipoImpuesto as TipoImpuestoSQL,
    TipoImpuestoDistribucion as TipoImpuestoDistribucionSQL,
    TipoImpuestoEtiqueta as TipoImpuestoEtiquetaSQL
)
from app.domain.entities.tipoimpuesto import TipoImpuesto
from app.domain.entities.tipo_impuesto_distribucion import TipoImpuestoDistribucion, TipoImpuestoEtiqueta
from app.domain.entities.condiciontributaria import CondicionTributaria as CondicionTributariaDomain
from app.domain.repository.tipoimpuesto_repository_interfase import TipoImpuestoRepositoryInterface
from app.domain.exceptions.tipoimpuesto import TipoImpuestoDuplicado, TipoImpuestoInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)

class TipoImpuestoRepositoryImpl(TipoImpuestoRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tipoimpuesto_id: int) -> Optional[TipoImpuesto]:
        stmt = (
            select(TipoImpuestoSQL)
            .options(
                selectinload(TipoImpuestoSQL.condiciones_asociadas),
                selectinload(TipoImpuestoSQL.reparticiones).joinedload(TipoImpuestoDistribucionSQL.etiqueta)
            )
            .where(TipoImpuestoSQL.id == tipoimpuesto_id)
        )
        result = await self.db.execute(stmt)
        tipoimpuesto_sql = result.scalar_one_or_none()
        return self._to_domain(tipoimpuesto_sql) if tipoimpuesto_sql else None

    async def get_all(self) -> List[TipoImpuesto]:
        stmt = (
            select(TipoImpuestoSQL)
            .options(
                selectinload(TipoImpuestoSQL.condiciones_asociadas),
                selectinload(TipoImpuestoSQL.reparticiones).joinedload(TipoImpuestoDistribucionSQL.etiqueta)
            )
        )
        result = await self.db.execute(stmt)
        tipoimpuestos_sql = result.scalars().all()
        return [self._to_domain(c) for c in tipoimpuestos_sql]

    async def create(self, tipoimpuesto: TipoImpuesto) -> TipoImpuesto:
        try:
            tipoimpuesto_sql = self._to_orm(tipoimpuesto)
            self.db.add(tipoimpuesto_sql)
            await self.db.commit()
            await self.db.refresh(tipoimpuesto_sql)
            return await self.get_by_id(tipoimpuesto_sql.id)

        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity Error: {e}")
            raise ErrorDeRepositorio("Error de integridad al crear tipoimpuesto")
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating TipoImpuesto: {e}")
            raise ErrorDeRepositorio("Error inesperado al crear tipoimpuesto")

    async def update(self, tipoimpuesto_id: int, tipoimpuesto: TipoImpuesto) -> Optional[TipoImpuesto]:
        try:
            tipoimpuesto_sql = await self.db.get(TipoImpuestoSQL, tipoimpuesto_id)
            if not tipoimpuesto_sql:
                return None

            for field, value in vars(tipoimpuesto).items():
                if value is not None and hasattr(tipoimpuesto_sql, field) and field not in ['condiciones_asociadas', 'reparticiones', 'id']:
                    setattr(tipoimpuesto_sql, field, value)
            
            # Handle reparticiones replacement
            if hasattr(tipoimpuesto, 'reparticiones'):
                tipoimpuesto_sql.reparticiones = [
                    TipoImpuestoDistribucionSQL(
                        tipo_reparticion=r.tipo_reparticion,
                        factor_porcentaje=r.factor_porcentaje,
                        basado_en=r.basado_en,
                        etiqueta_id=r.etiqueta_id,
                        cuenta_contable=r.cuenta_contable
                    ) for r in tipoimpuesto.reparticiones
                ]

            await self.db.commit()
            return await self.get_by_id(tipoimpuesto_id)

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating TipoImpuesto: {e}")
            raise ErrorDeRepositorio(f"Error inesperado al actualizar tipoimpuesto: {e}")

    async def delete(self, tipoimpuesto_id: int) -> None:
        try:
            tipoimpuesto_sql = await self.db.get(TipoImpuestoSQL, tipoimpuesto_id)
            if not tipoimpuesto_sql:
                return
            await self.db.delete(tipoimpuesto_sql)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting TipoImpuesto: {e}")
            raise ErrorDeRepositorio("Error inesperado al eliminar tipoimpuesto")

    async def get_by_afip_code(self, code: str) -> Optional[TipoImpuesto]:
        stmt = (
            select(TipoImpuestoSQL)
            .options(
                selectinload(TipoImpuestoSQL.condiciones_asociadas),
                selectinload(TipoImpuestoSQL.reparticiones).joinedload(TipoImpuestoDistribucionSQL.etiqueta)
            )
            .where(TipoImpuestoSQL.codigo_afip == code)
        )
        result = await self.db.execute(stmt)
        tipoimpuesto_sql = result.scalar_one_or_none()
        return self._to_domain(tipoimpuesto_sql) if tipoimpuesto_sql else None

    def _to_domain(self, tipoimpuesto_sql: TipoImpuestoSQL) -> TipoImpuesto:
        entity = TipoImpuesto(
            id=tipoimpuesto_sql.id,
            codigo_afip=tipoimpuesto_sql.codigo_afip,
            nombre=tipoimpuesto_sql.nombre,
            descripcion=tipoimpuesto_sql.descripcion,
            tipo_aplicacion=tipoimpuesto_sql.tipo_aplicacion,
            base_calculo=tipoimpuesto_sql.base_calculo,
            ambito=tipoimpuesto_sql.ambito,
            categoria=tipoimpuesto_sql.categoria,
            porcentaje=tipoimpuesto_sql.porcentaje,
            editable=tipoimpuesto_sql.editable,
            obligatorio=tipoimpuesto_sql.obligatorio,
            activo=tipoimpuesto_sql.activo,
            tipo_uso=tipoimpuesto_sql.tipo_uso,
            metodo_calculo=tipoimpuesto_sql.metodo_calculo,
            ambito_uso=tipoimpuesto_sql.ambito_uso,
            importe=tipoimpuesto_sql.importe,
            etiqueta_factura=tipoimpuesto_sql.etiqueta_factura,
            incluido_precio=tipoimpuesto_sql.incluido_precio,
            afecta_base_subsecuente=tipoimpuesto_sql.afecta_base_subsecuente,
            categoria_fiscal=tipoimpuesto_sql.categoria_fiscal,
            notas_legales=tipoimpuesto_sql.notas_legales,
            cuenta_impuesto_vta=tipoimpuesto_sql.cuenta_impuesto_vta,
            cuenta_impuesto_com=tipoimpuesto_sql.cuenta_impuesto_com
        )
        
        try:
            if tipoimpuesto_sql.condiciones_asociadas:
                entity.condiciones_asociadas = [
                    CondicionTributariaDomain(
                        id=c.id, 
                        nombre=c.nombre, 
                        descripcion=c.descripcion, 
                        ambito=c.ambito
                    ) for c in tipoimpuesto_sql.condiciones_asociadas
                ]
        except Exception:
            entity.condiciones_asociadas = []

        try:
            if tipoimpuesto_sql.reparticiones:
                entity.reparticiones = [
                    TipoImpuestoDistribucion(
                        id=r.id,
                        tipo_impuesto_id=r.tipo_impuesto_id,
                        tipo_reparticion=r.tipo_reparticion,
                        factor_porcentaje=r.factor_porcentaje,
                        basado_en=r.basado_en,
                        etiqueta_id=r.etiqueta_id,
                        cuenta_contable=r.cuenta_contable,
                        etiqueta=TipoImpuestoEtiqueta(
                            id=r.etiqueta.id,
                            nombre=r.etiqueta.nombre,
                            descripcion=r.etiqueta.descripcion
                        ) if r.etiqueta else None
                    ) for r in tipoimpuesto_sql.reparticiones
                ]
        except Exception:
            entity.reparticiones = []
            
        return entity

    def _to_orm(self, tipoimpuesto: TipoImpuesto) -> TipoImpuestoSQL:
        obj = TipoImpuestoSQL(
            id=tipoimpuesto.id,
            codigo_afip=tipoimpuesto.codigo_afip,
            nombre=tipoimpuesto.nombre,
            descripcion=tipoimpuesto.descripcion,
            tipo_aplicacion=tipoimpuesto.tipo_aplicacion,
            base_calculo=tipoimpuesto.base_calculo,
            ambito=tipoimpuesto.ambito,
            categoria=tipoimpuesto.categoria,
            porcentaje=tipoimpuesto.porcentaje,
            editable=tipoimpuesto.editable,
            obligatorio=tipoimpuesto.obligatorio,
            activo=tipoimpuesto.activo,
            tipo_uso=tipoimpuesto.tipo_uso,
            metodo_calculo=tipoimpuesto.metodo_calculo,
            ambito_uso=tipoimpuesto.ambito_uso,
            importe=tipoimpuesto.importe,
            etiqueta_factura=tipoimpuesto.etiqueta_factura,
            incluido_precio=tipoimpuesto.incluido_precio,
            afecta_base_subsecuente=tipoimpuesto.afecta_base_subsecuente,
            categoria_fiscal=tipoimpuesto.categoria_fiscal,
            notas_legales=tipoimpuesto.notas_legales,
            cuenta_impuesto_vta=tipoimpuesto.cuenta_impuesto_vta,
            cuenta_impuesto_com=tipoimpuesto.cuenta_impuesto_com
        )

        if tipoimpuesto.reparticiones:
            obj.reparticiones = [
                TipoImpuestoDistribucionSQL(
                    tipo_reparticion=r.tipo_reparticion,
                    factor_porcentaje=r.factor_porcentaje,
                    basado_en=r.basado_en,
                    etiqueta_id=r.etiqueta_id,
                    cuenta_contable=r.cuenta_contable
                ) for r in tipoimpuesto.reparticiones
            ]
        
        return obj
