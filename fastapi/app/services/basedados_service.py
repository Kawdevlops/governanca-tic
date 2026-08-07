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

from app.repositories.basedados_repo import BaseDadosRepository
from app.models.basedados import BaseDadosCreate, BaseDadosResponse, BaseDadosUpdate
from fastapi import HTTPException


class BaseDadosService:
    def __init__(self, repo: BaseDadosRepository):
        self.repo = repo

    async def listar_catalogo(self) -> list[BaseDadosResponse]:
        return await self.repo.listar()
    
    async def listar_orgaos_existentes(self) -> list[str]:
        return await self.repo.listar_orgaos_existentes()

    async def listar_setores_existentes(self, orgao: str | None = None) -> list[str]:
        return await self.repo.listar_setores_existentes(orgao)
    
    async def obter_por_titulo(self, titulo: str) -> BaseDadosResponse:
        base = await self.repo.obter_por_titulo(titulo)
        if not base:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return base

    async def criar(self, payload: BaseDadosCreate) -> BaseDadosResponse:
        existente = await self.repo.obter_por_titulo(payload.titulo)
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma base de dados cadastrada com este título."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, titulo: str, payload: BaseDadosUpdate) -> BaseDadosResponse:
        base = await self.repo.atualizar(titulo, payload)
        if not base:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return base

    async def deletar(self, titulo: str) -> dict:
        removido = await self.repo.deletar(titulo)
        if not removido:
            raise HTTPException(status_code=404, detail="Base de dados não encontrada.")
        return {"detail": "Base de dados removida com sucesso."}