from fastapi import APIRouter, Depends, status
from app.models.sistema import SistemaCreate, SistemaResponse
from app.services.sistema_service import SistemaService
from app.repositories.sistema_repo import SistemaRepository
from app.core.database import Neo4jConnection


router = APIRouter(prefix="/sistemas", tags=["Sistemas"])

def get_service() -> SistemaService:
    repo = SistemaRepository(Neo4jConnection.get_driver())
    return SistemaService(repo)

@router.post("/", response_model=SistemaResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    payload: SistemaCreate,
    service: SistemaService = Depends(get_service)
):
    return await service.criar(payload)
