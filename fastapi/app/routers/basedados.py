from fastapi import APIRouter, Depends, status, HTTPException
from app.models.basedados import BaseDadosCreate, BaseDadosResponse, BaseDadosUpdate
from app.services.basedados_service import BaseDadosService
from app.repositories.basedados_repo import BaseDadosRepository
from app.core.database import Neo4jConnection

router = APIRouter(prefix="/catalogo/bases-dados", tags=["Catálogo Municipal de Bases de Dados (CMBD)"])


def get_service() -> BaseDadosService:
    repo = BaseDadosRepository(Neo4jConnection.get_driver())
    return BaseDadosService(repo)


@router.get("/", response_model=list[BaseDadosResponse])
async def listar(service: BaseDadosService = Depends(get_service)):
    return await service.listar_catalogo()


@router.get("/obter-por-titulo", response_model=BaseDadosResponse)
async def obter_por_titulo(
    titulo: str, 
    service: BaseDadosService = Depends(get_service)
):
    resultado = await service.obter_por_titulo(titulo)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Base de dados com título '{titulo}' não encontrada"
        )
    return resultado


@router.post("/", response_model=BaseDadosResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    payload: BaseDadosCreate, 
    service: BaseDadosService = Depends(get_service)
):
    try:
        return await service.criar(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/", response_model=BaseDadosResponse)
async def atualizar(
    titulo: str,
    payload: BaseDadosUpdate,
    service: BaseDadosService = Depends(get_service)
):
    resultado = await service.atualizar(titulo, payload)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Base de dados com título '{titulo}' não encontrada"
        )
    return resultado


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(
    titulo: str,
    service: BaseDadosService = Depends(get_service)
):
    removido = await service.deletar(titulo)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Base de dados com título '{titulo}' não encontrada"
        )
    return None