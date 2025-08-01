from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repository.comprobante_repository_interfase import ComprobanteRepositoryInterface
from app.domain.repository.comprobantedetalle_repository_interfase import ComprobanteDetalleRepositoryInterface
from app.domain.repository.comprobanteimpuesto_repository_interfase import ComprobanteImpuestoRepositoryInterface
from app.repositories.comprobante_repository import ComprobanteRepositoryImpl
from app.repositories.comprobantedetalle_repository import ComprobanteDetalleRepositoryImpl
from app.repositories.comprobanteimpuesto_repository import ComprobanteImpuestoRepositoryImpl
import logging

logger = logging.getLogger(__name__)


class ComprobanteFullUOW:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._comprobante_repo: ComprobanteRepositoryInterface | None = None
        self._comprobante_detalle_repo: ComprobanteDetalleRepositoryInterface | None = None
        self._comprobante_impuesto_repo: ComprobanteImpuestoRepositoryInterface | None = None

    async def __aenter__(self):
        logger.debug("🟢 Iniciando unidad de trabajo comprobante")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            logger.warning("🔴 Rollback por excepción en UOW: %s", exc_type)
            await self.rollback()
        else:
            logger.info("🟢 Commit exitoso en UOW")
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()

    @property
    def comprobante_repo(self) -> ComprobanteRepositoryInterface:
        if self._comprobante_repo is None:
            self._comprobante_repo = ComprobanteRepositoryImpl(self.session)
        return self._comprobante_repo

    @property
    def comprobante_detalle_repo(self) -> ComprobanteDetalleRepositoryInterface:
        if self._comprobante_detalle_repo is None:
            self._comprobante_detalle_repo = ComprobanteDetalleRepositoryImpl(self.session)
        return self._comprobante_detalle_repo

    @property
    def comprobante_impuesto_repo(self) -> ComprobanteImpuestoRepositoryInterface:
        if self._comprobante_impuesto_repo is None:
            self._comprobante_impuesto_repo = ComprobanteImpuestoRepositoryImpl(self.session)
        return self._comprobante_impuesto_repo
