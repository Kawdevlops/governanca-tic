from fastapi import APIRouter, Depends, status
from app.core.database import Neo4jConnection
from app.models.risco import RiscoCreate, RiscoUpdate, RiscoResponse, RiscoVinculo
from app.repositories.risco_repo import RiscoRepository
from app.services.risco_service import RiscoService


router = APIRouter(prefix="/risco", tags=["Risco"])


def get_service() -> RiscoService:
    repo = RiscoRepository(Neo4jConnection.get_driver())
    return RiscoService(repo)


@router.post("/", response_model=RiscoResponse, status_code=status.HTTP_201_CREATED)
async def criar(payload: RiscoCreate, service: RiscoService = Depends(get_service)):
    return await service.criar(payload)


@router.get("/", response_model=list[RiscoResponse])
async def listar(service: RiscoService = Depends(get_service)):
    return await service.listar()


# IMPORTANTE: precisa vir antes de /{identificador}
@router.get("/metricas")
async def metricas(service: RiscoService = Depends(get_service)):
    return await service.metricas()


@router.get("/{identificador}", response_model=RiscoResponse)
async def obter_por_identificador(
    identificador: str,
    service: RiscoService = Depends(get_service)
):
    return await service.obter_por_identificador(identificador)


@router.put("/{identificador}", response_model=RiscoResponse)
async def atualizar(
    identificador: str,
    dados_novos: RiscoUpdate,
    service: RiscoService = Depends(get_service)
):
    return await service.atualizar(identificador, dados_novos)


@router.delete("/{identificador}")
async def deletar(
    identificador: str,
    service: RiscoService = Depends(get_service)
):
    return await service.deletar(identificador)


@router.post("/{identificador}/vincular")
async def vincular_risco(
    identificador: str,
    vinculo: RiscoVinculo,
    service: RiscoService = Depends(get_service)
):
    return await service.vincular(identificador, vinculo)
