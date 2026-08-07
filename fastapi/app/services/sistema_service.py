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
from app.repositories.sistema_repo import SistemaRepository
from app.models.sistema import SistemaCreate, SistemaResponse

class SistemaService:
    
    def __init__(self, repo: SistemaRepository):
        self.repo = repo

    async def criar(self, payload: SistemaCreate) -> SistemaResponse:
        sistema_existente = await self.repo.obter_por_sigla(str(payload.sigla))
        if sistema_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um sistema com esta sigla."
            )
        return await self.repo.criar(payload)