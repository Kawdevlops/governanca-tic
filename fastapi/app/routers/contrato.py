from fastapi import APIRouter, Depends, status
from app.models.contrato import ContratoCreate, ContratoUpdate, ContratoResponse
from app.models.contrato_servico import ContratoServico, VinculoContratoServico
from app.services.contrato_service import ContratoService
from app.services.contrato_servico_service import ContratoServicoService
from app.repositories.contrato_repo import ContratoRepository
from app.repositories.servico_repo import ServicoRepository
from app.core.database import Neo4jConnection

router = APIRouter(prefix="/contratos", tags=["Contratos"])


def get_service() -> ContratoService:
    repo = ContratoRepository(Neo4jConnection.get_driver())
    return ContratoService(repo)


def get_services_contrato_servico() -> ContratoServicoService:
    repo_contrato = ContratoRepository(Neo4jConnection.get_driver())
    repo_servico = ServicoRepository(Neo4jConnection.get_driver())
    return ContratoServicoService(repo_servico=repo_servico, repo_contrato=repo_contrato)


@router.get("/", response_model=list[ContratoResponse])
async def listar(service: ContratoService = Depends(get_service)):
    return await service.listar()


@router.get("/{ano}/{numero}", response_model=ContratoResponse)
async def obter_por_numero_ano(numero: int, ano: int,
    service: ContratoService = Depends(get_service)):
    return await service.obter_por_numero_ano(numero, ano)


@router.post("/", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    payload: ContratoCreate,
    service: ContratoService = Depends(get_service)):
    return await service.criar(payload)


@router.post("/vinculo-servico", response_model=ContratoServico, status_code=status.HTTP_201_CREATED)
async def vincular_servico(
    numero: int, 
    ano: int, 
    vinculo: VinculoContratoServico,
    nome: str,
    service: ContratoServicoService = Depends(get_services_contrato_servico)
):
    return await service.vincular_servico(numero, ano, vinculo, nome)


@router.put("/{ano}/{numero}", response_model=ContratoResponse)
async def atualizar(
    numero: int, ano: int,
    payload: ContratoUpdate,
    service: ContratoService = Depends(get_service)
):
    return await service.atualizar(numero, ano, payload)


@router.delete("/{ano}/{numero}", status_code=status.HTTP_200_OK)
async def deletar(numero: int, ano: int, service: ContratoService = Depends(get_service)):
    return await service.deletar(numero, ano)