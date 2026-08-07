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

# app/models/pessoa.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.vinculo import Vinculo

DESCRICOES_PESSOA = {
    "nome" : "Nome completo da pessoa.",
    "email" : "Endereço eletrônico institucional.",
    "telefone_movel" : "Número do telefone móvel com DDD, por exemplo: (11) 9145-5401.",
    "telefone_fixo" : "Número do telefone fixo institucional.",
    "ramal" : "Número do ramal relacionado ao telefone fixo institucional"
}

class PessoaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150, description=DESCRICOES_PESSOA.get("nome"))
    email: EmailStr = Field(..., description=DESCRICOES_PESSOA.get("email"))
    telefone_movel: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_movel"))
    telefone_fixo: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_fixo"))
    ramal: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("ramal"))


class PessoaVinculos(PessoaBase):
    vinculos: list[Vinculo] = Field(default_factory=list)


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150, description=DESCRICOES_PESSOA.get("nome"))
    email: Optional[EmailStr] = Field(None, description=DESCRICOES_PESSOA.get("email"))
    telefone_movel: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_movel"))
    telefone_fixo: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("telefone_fixo"))
    ramal: Optional[str] = Field(None, description=DESCRICOES_PESSOA.get("ramal"))


class PessoaResponse(PessoaVinculos):
    element_id: str