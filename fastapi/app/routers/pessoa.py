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

from fastapi import APIRouter, Depends, status
from app.models.pessoa import PessoaCreate, PessoaUpdate, PessoaResponse
from app.models.pessoa_contrato import PessoaContrato, VinculoPessoaContrato
from app.services.pessoa_service import PessoaService
from app.services.pessoa_contrato_service import PessoaContratoService
from app.repositories.pessoa_repo import PessoaRepository
from app.repositories.contrato_repo import ContratoRepository
from app.core.database import Neo4jConnection

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])


def get_service() -> PessoaService:
    repo = PessoaRepository(Neo4jConnection.get_driver())
    return PessoaService(repo)

def get_services_pessoa_contrato() -> PessoaContratoService:
    repo_pessoa = PessoaRepository(Neo4jConnection.get_driver())
    repo_contrato = ContratoRepository(Neo4jConnection.get_driver())
    return PessoaContratoService(repo_pessoa=repo_pessoa, repo_contrato=repo_contrato)

@router.get("/", response_model=list[PessoaResponse])
async def listar(service: PessoaService = Depends(get_service)):
    return await service.listar()


@router.get("/{email}", response_model=PessoaResponse)
async def obter_por_email(
    email: str,
    service: PessoaService = Depends(get_service)
):
    return await service.obter_por_email(email)


@router.post("/", response_model=PessoaResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    payload: PessoaCreate,
    service: PessoaService = Depends(get_service)
):
    return await service.criar(payload)


@router.post("/{email}/vinculo-contrato", response_model=PessoaContrato, status_code=status.HTTP_201_CREATED)
async def vincular_pessoa(
    email: str, 
    vinculo: VinculoPessoaContrato, 
    numero: int, 
    ano: int, 
    service: PessoaContratoService = Depends(get_services_pessoa_contrato)
):
    return await service.vincular_contrato(email, vinculo, numero, ano)


@router.put("/{email}", response_model=PessoaResponse)
async def atualizar(
    email: str,
    payload: PessoaUpdate,
    service: PessoaService = Depends(get_service)
):
    return await service.atualizar(email, payload)


@router.delete("/{email}", status_code=status.HTTP_200_OK)
async def deletar(
    email: str,
    service: PessoaService = Depends(get_service)
):
    return await service.deletar(email)