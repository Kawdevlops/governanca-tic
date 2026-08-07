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

from fastapi import HTTPException
from app.repositories.pessoa_repo import PessoaRepository
from app.models.pessoa import PessoaCreate, PessoaUpdate, PessoaResponse

class PessoaService:
    def __init__(self, repo: PessoaRepository):
        self.repo = repo

    async def listar(self) -> list[PessoaResponse]:
        return await self.repo.listar()

    async def obter_por_email(self, email: str) -> PessoaResponse:
        pessoa = await self.repo.obter_por_email(email)
        if not pessoa:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return pessoa

    async def criar(self, payload: PessoaCreate) -> PessoaResponse:
        existente = await self.repo.obter_por_email(str(payload.email))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe uma pessoa com este e-mail."
            )
        return await self.repo.criar(payload)

    async def atualizar(self, email: str, payload: PessoaUpdate) -> PessoaResponse:
        pessoa = await self.repo.atualizar(email, payload)
        if not pessoa:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return pessoa

    async def deletar(self, email: str) -> dict:
        removido = await self.repo.deletar(email)
        if not removido:
            raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        return {"detail": "Pessoa removida com sucesso."}
    


