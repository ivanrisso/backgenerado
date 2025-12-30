
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.db.orm_models import Imputacion as ImputacionSQL
from app.domain.entities.imputacion import Imputacion
from app.domain.exceptions.base import ErrorDeRepositorio
import logging

logger = logging.getLogger(__name__)

class ImputacionRepositoryImpl:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, imputacion: Imputacion, commit: bool = True) -> Imputacion:
        try:
            imputacion_sql = ImputacionSQL(
                comprobante_credito_id=imputacion.comprobante_credito_id,
                comprobante_debito_id=imputacion.comprobante_debito_id,
                importe=imputacion.importe,
                fecha=imputacion.fecha
            )
            self.db.add(imputacion_sql)
            
            if commit:
                await self.db.commit()
                await self.db.refresh(imputacion_sql)
            else:
                await self.db.flush()
                
            imputacion.id = imputacion_sql.id
            return imputacion
            
        except Exception as e:
            logger.exception("Error al crear imputacion")
            raise ErrorDeRepositorio("Error al crear imputacion")
