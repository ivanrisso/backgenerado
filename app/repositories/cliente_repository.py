from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.infrastructure.db.orm_models import Cliente as ClienteSQL
from app.domain.entities.cliente import Cliente as ClienteDomain
from app.domain.repository.cliente_repository_interfase import ClienteRepositoryInterface


class ClienteRepositoryImpl(ClienteRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, cliente_id: int) -> Optional[ClienteDomain]:
        stmt = select(ClienteSQL).where(ClienteSQL.id == cliente_id)
        result = await self.db.execute(stmt)
        cliente_sql = result.scalar_one_or_none()
        return self._to_domain(cliente_sql) if cliente_sql else None

    async def get_all(self) -> List[ClienteDomain]:
        stmt = select(ClienteSQL)
        result = await self.db.execute(stmt)
        clientes_sql = result.scalars().all()
        return [self._to_domain(c) for c in clientes_sql]

    async def create(self, cliente: ClienteDomain) -> ClienteDomain:
        cliente_sql = self._to_orm(cliente)
        self.db.add(cliente_sql)
        await self.db.commit()
        await self.db.refresh(cliente_sql)
        return self._to_domain(cliente_sql)

    async def update(self, cliente_id: int, cliente: ClienteDomain) -> ClienteDomain:
        # Opcionalmente podrías usar cliente_id para verificar existencia
        cliente_sql = self._to_orm(cliente)
        self.db.add(cliente_sql)
        await self.db.commit()
        await self.db.refresh(cliente_sql)
        return self._to_domain(cliente_sql)

    async def delete(self, cliente_id: int) -> None:
        stmt = select(ClienteSQL).where(ClienteSQL.id == cliente_id)
        result = await self.db.execute(stmt)
        cliente_sql = result.scalar_one_or_none()
        if cliente_sql:
            await self.db.delete(cliente_sql)
            await self.db.commit()

    # Métodos de mapeo
    def _to_domain(self, cliente_sql: ClienteSQL) -> ClienteDomain:
        return ClienteDomain(
            id=cliente_sql.id,
            nombre=cliente_sql.nombre,
            apellido=cliente_sql.apellido,
            cuit=cliente_sql.cuit,
            email=cliente_sql.email,
            tipo_doc_id=cliente_sql.tipo_doc_id,
            iva_id=cliente_sql.iva_id,
        )

    def _to_orm(self, cliente: ClienteDomain) -> ClienteSQL:
        return ClienteSQL(
            id=cliente.id,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            cuit=cliente.cuit,
            email=cliente.email,
            tipo_doc_id=cliente.tipo_doc_id,
            iva_id=cliente.iva_id,
        )
