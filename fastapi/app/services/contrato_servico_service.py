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
from app.models.contrato_servico import ContratoServico, VinculoContratoServico
from app.repositories.contrato_repo import ContratoRepository
from app.repositories.servico_repo import ServicoRepository

class ContratoServicoService():

    def __init__(self, repo_contrato: ContratoRepository, repo_servico: ServicoRepository):
        self.repo_servico = repo_servico
        self.repo_contrato = repo_contrato

    async def vincular_servico(self, numero:int , ano:int, vinculo: VinculoContratoServico, nome: str) -> ContratoServico:
        contrato = await self.repo_contrato.obter_por_numero_ano(numero, ano)
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado.")
        servico = await self.repo_servico.obter_por_nome_servico(nome)        
        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado.")
        
        vinculado = await self.repo_contrato.vincular_servico(contrato, servico, vinculo)
        if not vinculado:
            raise HTTPException(status_code=500, detail="Não foi possível vincular o contrato ao serviço.")
        return vinculado

