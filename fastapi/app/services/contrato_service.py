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
from app.repositories.contrato_repo import ContratoRepository
from app.models.contrato import ContratoCreate, ContratoUpdate, ContratoResponse

class ContratoService:
    def __init__(self, repo: ContratoRepository):
        self.repo = repo
    
    async def listar(self) -> list[ContratoResponse]:
        return await self.repo.listar()

    async def obter_por_numero_ano(self, numero: int, ano: int) -> ContratoResponse:
        contrato = await self.repo.obter_por_numero_ano(numero, ano)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return contrato

    async def criar(self, payload: ContratoCreate) -> ContratoResponse:
        existente = await self.repo.obter_por_numero_ano(int(payload.numero), int(payload.ano))
        if existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um contrato com este número e ano."
            )
        return await self.repo.criar(payload)
    
    async def atualizar(self, numero: int, ano: int, payload: ContratoUpdate) -> ContratoResponse:
        contrato = await self.repo.atualizar(numero, ano, payload)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return contrato
        
    async def deletar(self, numero: int, ano: int) -> dict:
        removido = await self.repo.deletar(numero, ano)
        if not removido:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        return {"detail": "Contrato removido com sucesso."}