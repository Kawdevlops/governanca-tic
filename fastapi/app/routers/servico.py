from fastapi import APIRouter, Depends, status
from app.models.servico import ServicoCreate, ServicoResponse, ServicoUpdate
from app.services.servico_service import ServicoService
from app.repositories.servico_repo import ServicoRepository
from app.core.database import Neo4jConnection

router = APIRouter(prefix="/catalogo/servicos", tags=["Catálogo de Serviços TIC"])

def get_service() -> ServicoService:
    repo = ServicoRepository(Neo4jConnection.get_driver())
    return ServicoService(repo)

@router.get("/", response_model=list[ServicoResponse])
async def listar(service: ServicoService = Depends(get_service)):
    return await service.listar_catalogo()

@router.get("/obter-por-nome", response_model=ServicoResponse)
async def obter_por_nome_servico(nome: str, service: ServicoService = Depends(get_service)):
    return await service.obter_por_nome_servico(nome)

@router.post("/", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
async def criar(payload: ServicoCreate, service: ServicoService = Depends(get_service)):
    return await service.criar(payload)

@router.put("/", response_model=ServicoResponse)
async def atualizar(
    nome: str,
    payload: ServicoUpdate,
    service: ServicoService = Depends(get_service)
):
    return await service.atualizar(nome, payload)

@router.delete("/", status_code=status.HTTP_200_OK)
async def deletar(
    nome: str,
    service: ServicoService = Depends(get_service)
):
    return await service.deletar(nome)