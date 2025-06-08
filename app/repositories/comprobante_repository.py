# ✅ app/repositories/comprobante_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from typing import Optional, List

from app.infrastructure.db.orm_models import Comprobante as ComprobanteSQL
from app.domain.entities.comprobante import Comprobante
from app.domain.repository.comprobante_repository_interfase import ComprobanteRepositoryInterface
from app.domain.exceptions.comprobante import ComprobanteDuplicado, ComprobanteInvalido
from app.domain.exceptions.base import BaseDeDatosNoDisponible, ErrorDeRepositorio
from app.domain.exceptions.integridad import ClaveForaneaInvalida

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class ComprobanteRepositoryImpl(ComprobanteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comprobante_id: int) -> Optional[Comprobante]:
        stmt = select(ComprobanteSQL).where(ComprobanteSQL.id == comprobante_id)
        result = await self.db.execute(stmt)
        comprobante_sql = result.scalar_one_or_none()
        return self._to_domain(comprobante_sql) if comprobante_sql else None

    async def get_all(self) -> List[Comprobante]:
        stmt = select(ComprobanteSQL)
        result = await self.db.execute(stmt)
        comprobantes_sql = result.scalars().all()
        return [self._to_domain(c) for c in comprobantes_sql]

    async def create(self, comprobante: Comprobante) -> Comprobante:
        try:
            comprobante_sql = self._to_orm(comprobante)
            self.db.add(comprobante_sql)
            await self.db.commit()
            await self.db.refresh(comprobante_sql)
            return self._to_domain(comprobante_sql)

        except IntegrityError as e:
                        
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteDuplicado("numero", str(comprobante.numero))

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(comprobante.cliente_id))
                    elif "tipo_comprobante_id" in msg:
                        raise ClaveForaneaInvalida("tipo_comprobante_id", str(comprobante.tipo_comprobante_id))
                    elif "concepto_id" in msg:
                        raise ClaveForaneaInvalida("concepto_id", str(comprobante.concepto_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(comprobante.tipo_doc_id))
                    elif "moneda_id" in msg:
                        raise ClaveForaneaInvalida("moneda_id", str(comprobante.moneda_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")
                                                
            logger.info("Error de integridad al crear comprobante")
            raise ErrorDeRepositorio("Error de integridad al crear comprobante")
        
        except DataError as da:
            
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteInvalido(msg)   
            
            raise ComprobanteInvalido(msg)   
                 
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception as exc:
            raise ErrorDeRepositorio("Error inesperado al crear comprobante")

    async def update(self, comprobante_id: int, comprobante: Comprobante) -> Optional[Comprobante]:
        try:
            comprobante_sql = await self.db.get(ComprobanteSQL, comprobante_id)
            if not comprobante_sql:
                return None

            cambios = False
            for field, value in vars(comprobante).items():
                if value is not None and hasattr(comprobante_sql, field):
                    setattr(comprobante_sql, field, value)
                    cambios = True

            if cambios:
                await self.db.commit()
                await self.db.refresh(comprobante_sql)

            return self._to_domain(comprobante_sql)

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                msg = msg.lower()

                if error_code == 1062:
                    raise ComprobanteDuplicado("numero", str(comprobante.numero))

                elif error_code == 1452:
                    if "cliente_id" in msg:
                        raise ClaveForaneaInvalida("cliente_id", str(comprobante.cliente_id))
                    elif "tipo_comprobante_id" in msg:
                        raise ClaveForaneaInvalida("tipo_comprobante_id", str(comprobante.tipo_comprobante_id))
                    elif "concepto_id" in msg:
                        raise ClaveForaneaInvalida("concepto_id", str(comprobante.concepto_id))
                    elif "tipo_doc_id" in msg:
                        raise ClaveForaneaInvalida("tipo_doc_id", str(comprobante.tipo_doc_id))
                    elif "moneda_id" in msg:
                        raise ClaveForaneaInvalida("moneda_id", str(comprobante.moneda_id))
                    else:
                        raise ClaveForaneaInvalida("campo_desconocido")

            raise ErrorDeRepositorio("Error de integridad al actualizar comprobante")
        except DataError as da:
            if hasattr(da.orig, "args"):
                error_code, msg = da.orig.args
                raise ComprobanteInvalido(msg)   
            
        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al actualizar comprobante")


    async def delete(self, comprobante_id: int) -> None:
        try:
            comprobante_sql = await self.db.get(ComprobanteSQL, comprobante_id)
            if not comprobante_sql:
                return

            await self.db.delete(comprobante_sql)
            await self.db.commit()

        except IntegrityError as e:
            if hasattr(e.orig, "args"):
                error_code, msg = e.orig.args
                if error_code == 1451:
                    raise ClaveForaneaInvalida("comprobante_id", str(comprobante_id))

            raise ErrorDeRepositorio("Error de integridad al eliminar comprobante")

        except OperationalError:
            raise BaseDeDatosNoDisponible()
        except Exception:
            raise ErrorDeRepositorio("Error inesperado al eliminar comprobante")

    def _to_domain(self, comprobante_sql: ComprobanteSQL) -> Comprobante:
        return Comprobante(
            id=comprobante_sql.id,
            cliente_id=comprobante_sql.cliente_id,
            tipo_comprobante_id=comprobante_sql.tipo_comprobante_id,
            concepto_id=comprobante_sql.concepto_id,
            tipo_doc_id=comprobante_sql.tipo_doc_id,
            moneda_id=comprobante_sql.moneda_id,
            punto_venta=comprobante_sql.punto_venta,
            numero=comprobante_sql.numero,            
            fecha_emision=comprobante_sql.fecha_emision,
            doc_nro=comprobante_sql.doc_nro,
            nombre_cliente=comprobante_sql.nombre_cliente,
            cuit_cliente=comprobante_sql.cuit_cliente,
            domicilio_cliente=comprobante_sql.domicilio_cliente,
            localidad_cliente=comprobante_sql.localidad_cliente,
            cod_postal_cliente=comprobante_sql.cod_postal_cliente,            
            provincia_cliente=comprobante_sql.provincia_cliente,
            cotizacion_moneda=comprobante_sql.cotizacion_moneda,
            total_neto=comprobante_sql.total_neto,
            total_iva=comprobante_sql.total_iva,
            total_impuestos=comprobante_sql.total_impuestos,
            total=comprobante_sql.total,
            observaciones=comprobante_sql.observaciones            
        )


    def _to_orm(self, comprobante: Comprobante) -> ComprobanteSQL:
        return ComprobanteSQL(
            id=comprobante.id,
            cliente_id=comprobante.cliente_id,
            tipo_comprobante_id=comprobante.tipo_comprobante_id,
            concepto_id=comprobante.concepto_id,
            tipo_doc_id=comprobante.tipo_doc_id,
            moneda_id=comprobante.moneda_id,
            punto_venta=comprobante.punto_venta,
            numero=comprobante.numero,            
            fecha_emision=comprobante.fecha_emision,
            doc_nro=comprobante.doc_nro,
            nombre_cliente=comprobante.nombre_cliente,
            cuit_cliente=comprobante.cuit_cliente,
            domicilio_cliente=comprobante.domicilio_cliente,
            localidad_cliente=comprobante.localidad_cliente,
            cod_postal_cliente=comprobante.cod_postal_cliente,            
            provincia_cliente=comprobante.provincia_cliente,
            cotizacion_moneda=comprobante.cotizacion_moneda,
            total_neto=comprobante.total_neto,
            total_iva=comprobante.total_iva,
            total_impuestos=comprobante.total_impuestos,
            total=comprobante.total,
            observaciones=comprobante.observaciones            
            
        )
        
