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

from app.repositories.servico_repo import ServicoRepository
from app.models.servico import ServicoCreate, ServicoResponse, ServicoUpdate
from fastapi import HTTPException

class ServicoService:
    def __init__(self, repo: ServicoRepository):
        self.repo = repo

    async def listar_catalogo(self) -> list[ServicoResponse]:
        return await self.repo.listar()
    
    async def obter_por_nome_servico(self, nome: str) -> ServicoResponse:
        servico = await self.repo.obter_por_nome_servico(nome)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return servico

    async def criar(self, payload: ServicoCreate) -> ServicoResponse:
        existente = await self.repo.obter_por_nome_servico(str(payload.nome))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um serviço com este nome."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, nome: str, payload: ServicoUpdate) -> ServicoUpdate:
        servico = await self.repo.atualizar(nome, payload)
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return servico
    
    async def deletar(self, nome: str) -> dict:
        removido = await self.repo.deletar(nome)
        if not removido:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        return {"detail": "Serviço removido com sucesso."}
