# Projeto Hydra - Isto faz aquilo o qual se pretende fazer
# Copyright (C) 2026 Secretaria Municipal das Subprefeituras
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from fastapi import APIRouter, Depends, status, HTTPException
from app.models.basedados import BaseDadosCreate, BaseDadosResponse, BaseDadosUpdate
from app.services.basedados_service import BaseDadosService
from app.repositories.basedados_repo import BaseDadosRepository
from app.core.database import Neo4jConnection

router = APIRouter(prefix="/catalogo/bases-dados", tags=["Catálogo Bases de Dados TIC "])


def get_service() -> BaseDadosService:
    repo = BaseDadosRepository(Neo4jConnection.get_driver())
    return BaseDadosService(repo)

# @router.get esta função responde a requisições HTTP do tipo GET
@router.get("/", response_model=list[BaseDadosResponse])
async def listar(service: BaseDadosService = Depends(get_service)):
    return await service.listar_catalogo()

@router.get("/orgaos-existentes", response_model=list[str])
async def orgaos_existentes(service: BaseDadosService = Depends(get_service)):
    return await service.listar_orgaos_existentes()

@router.get("/setores-existentes", response_model=list[str])
async def setores_existentes(orgao: str | None = None, service: BaseDadosService = Depends(get_service)):
    return await service.listar_setores_existentes(orgao)

@router.get("/obter-por-titulo", response_model=BaseDadosResponse) # titulo endereço do endpoint, e devolve a estrutura do response
async def obter_por_titulo(titulo: str, service: BaseDadosService = Depends(get_service)): 
    resultado = await service.obter_por_titulo(titulo)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Base de dados com título '{titulo}' não encontrada")
    return resultado


@router.post("/", response_model=BaseDadosResponse, status_code=status.HTTP_201_CREATED)
async def criar(payload: BaseDadosCreate, service: BaseDadosService = Depends(get_service)):
    try:
        return await service.criar(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


@router.put("/", response_model=BaseDadosResponse)
async def atualizar(titulo: str,payload: BaseDadosUpdate,service: BaseDadosService = Depends(get_service)):
    resultado = await service.atualizar(titulo, payload)
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Base de dados com título '{titulo}' não encontrada")
    return resultado


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(titulo: str,service: BaseDadosService = Depends(get_service)):
    removido = await service.deletar(titulo)
    if not removido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Base de dados com título '{titulo}' não encontrada")
    return None