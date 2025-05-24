from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List

from app.infrastructure.db.engine import SessionLocal
from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Cliente"])

# Dependency para obtener sesión de base de datos
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# Listar todos los clientes
@router.get("/", response_model=List[ClienteResponse])
async def get_all(db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.get_all()

# Obtener cliente por ID
@router.get("/{id}", response_model=ClienteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    cliente = await service.get_by_id(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Crear nuevo cliente
@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ClienteCreate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.create(data)

# Actualizar cliente existente
@router.put("/{id}", response_model=ClienteResponse)
async def update(id: int, data: ClienteUpdate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    cliente = await service.update(id, data)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Eliminar cliente por ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    cliente = await service.get_by_id(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    await service.delete(id)
