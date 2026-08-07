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

from pydantic import BaseModel, Field
from typing import Optional

DESCRICOES_SISTEMA = {
    "nome" : "Nome do sistema. Por exemplo: Sistema de Gerenciamento de Zeladoria",
    "sigla" : "Sigla do sistema. Por exemplo: SGZ"
}

class SistemaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_SISTEMA.get("nome"))
    sigla : str = Field(..., min_length=3, max_length=50, description=DESCRICOES_SISTEMA.get("sigla"))


class SistemaCreate(SistemaBase):
    pass


class SistemaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_SISTEMA.get("nome"))
    sigla: Optional[str] = Field(None, min_length=3, max_length=50, description=DESCRICOES_SISTEMA.get("sigla"))


class SistemaResponse(SistemaBase):
    element_id: str