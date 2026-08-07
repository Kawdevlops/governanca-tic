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
from app.models.sistema import SistemaCreate, SistemaResponse
from app.services.sistema_service import SistemaService
from app.repositories.sistema_repo import SistemaRepository
from app.core.database import Neo4jConnection


router = APIRouter(prefix="/sistemas", tags=["Sistemas"])

def get_service() -> SistemaService:
    repo = SistemaRepository(Neo4jConnection.get_driver())
    return SistemaService(repo)

@router.post("/", response_model=SistemaResponse, status_code=status.HTTP_201_CREATED)
async def criar(
    payload: SistemaCreate,
    service: SistemaService = Depends(get_service)
):
    return await service.criar(payload)
