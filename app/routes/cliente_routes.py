from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.engine import SessionLocal
from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Cliente"])

async def get_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ClienteResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.list_all()

@router.get("/{id}", response_model=ClienteResponse)
async def get_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.get_by_id(id)

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create(data: ClienteCreate, db: AsyncSession = Depends(get_db_session)):
    service = ClienteService(db)
    return await service.create(data)